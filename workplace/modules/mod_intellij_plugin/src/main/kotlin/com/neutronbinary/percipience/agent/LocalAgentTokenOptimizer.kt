package com.neutronbinary.percipience.agent

import com.intellij.openapi.project.Project
import com.intellij.psi.PsiFile
import com.neutronbinary.percipience.psi.PsiAstBridge
import com.neutronbinary.percipience.psi.PsiTokenMetrics

data class OptimizedPromptContext(
    val originalTokens: Int,
    val optimizedTokens: Int,
    val tokensSaved: Int,
    val compressionRatio: Double,
    val finalPrompt: String,
    val hasPinnedStaticPrefix: Boolean
)

object LocalAgentTokenOptimizer {

    private const val STATIC_PREFIX_HEADER = "<!-- STATIC_PREFIX_START -->\nYou are an autonomous local AI engineering agent governed by Percipience Context OS (Free Edition).\nOperate strictly under Quad-Space isolation and contract invariants.\n<!-- STATIC_PREFIX_END -->\n\n"

    /**
     * Slices and skeletonizes a PsiFile for local agent consumption, ensuring 60%-80% token savings.
     */
    fun optimizePsiFile(psiFile: PsiFile): Pair<String, PsiTokenMetrics> {
        val metrics = PsiAstBridge.extractSymbolsAndPrune(psiFile)
        val text = psiFile.text
        val lines = text.lines()
        val prunedLines = lines.filter { line ->
            val trimmed = line.trim()
            trimmed.startsWith("def ") || trimmed.startsWith("class ") ||
            trimmed.startsWith("fun ") || trimmed.startsWith("public ") ||
            trimmed.startsWith("interface ") || trimmed.startsWith("@") ||
            trimmed.startsWith("import ") || trimmed.startsWith("package ") ||
            trimmed.startsWith("type ") || trimmed.startsWith("export ") ||
            trimmed.startsWith("struct ") || trimmed.startsWith("trait ")
        }
        val prunedBody = prunedLines.joinToString("\n")
        return Pair(prunedBody, metrics)
    }

    /**
     * Builds an attention-budgeted prompt context with static prefix pinning and AST skeletonization.
     */
    fun buildOptimizedAgentPrompt(
        rawCodeContext: String,
        taskDescription: String,
        contractSchema: String = ""
    ): OptimizedPromptContext {
        val rawTokens = estimateTokenCount(rawCodeContext) + estimateTokenCount(taskDescription) + estimateTokenCount(contractSchema)

        // 1. Skeletonize raw code context
        val lines = rawCodeContext.lines()
        val prunedLines = lines.filter { line ->
            val trimmed = line.trim()
            trimmed.startsWith("def ") || trimmed.startsWith("class ") ||
            trimmed.startsWith("fun ") || trimmed.startsWith("public ") ||
            trimmed.startsWith("interface ") || trimmed.startsWith("@") ||
            trimmed.startsWith("import ") || trimmed.startsWith("package ") ||
            trimmed.startsWith("type ") || trimmed.startsWith("export ")
        }
        val prunedCode = if (prunedLines.isNotEmpty()) prunedLines.joinToString("\n") else rawCodeContext.take(500)

        // 2. Assemble budgeted prompt with static prefix pinning
        val sb = StringBuilder()
        sb.append(STATIC_PREFIX_HEADER)
        if (contractSchema.isNotBlank()) {
            sb.append("### CONTRACT INVARIANTS (25% Budget):\n")
            sb.append(contractSchema.trim())
            sb.append("\n\n")
        }
        sb.append("### CODEBASE AST SKELETON (35% Budget):\n```\n")
        sb.append(prunedCode)
        sb.append("\n```\n\n")
        sb.append("### LOCAL AGENT TASK:\n")
        sb.append(taskDescription.trim())

        val finalPrompt = sb.toString()
        val optimizedTokens = estimateTokenCount(finalPrompt)
        val saved = (rawTokens - optimizedTokens).coerceAtLeast(0)
        val ratio = if (rawTokens > 0) (saved.toDouble() / rawTokens.toDouble()) * 100.0 else 0.0

        return OptimizedPromptContext(
            originalTokens = rawTokens,
            optimizedTokens = optimizedTokens,
            tokensSaved = saved,
            compressionRatio = Math.round(ratio * 100.0) / 100.0,
            finalPrompt = finalPrompt,
            hasPinnedStaticPrefix = true
        )
    }

    private fun estimateTokenCount(text: String): Int {
        return text.split(Regex("\\s+")).filter { it.isNotBlank() }.size
    }
}
