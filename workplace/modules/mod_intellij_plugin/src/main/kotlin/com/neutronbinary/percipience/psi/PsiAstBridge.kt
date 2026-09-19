package com.neutronbinary.percipience.psi

import com.intellij.psi.PsiFile
import java.util.concurrent.ConcurrentHashMap

data class PsiTokenMetrics(
    val originalTokens: Int,
    val prunedTokens: Int,
    val savedTokens: Int,
    val reductionPercentage: Double,
    val traversalMs: Long
)

class PsiAstBridge {
    companion object {
        fun extractSymbolsAndPrune(psiFile: PsiFile): PsiTokenMetrics {
            val startTime = System.currentTimeMillis()
            val text = psiFile.text
            val lines = text.lines()
            val originalTokens = text.split(Regex("\\s+")).filter { it.isNotBlank() }.size

            // Synthetic AST extraction stripping function/method bodies
            val prunedLines = lines.filter { line ->
                val trimmed = line.trim()
                trimmed.startsWith("def ") || trimmed.startsWith("class ") ||
                trimmed.startsWith("fun ") || trimmed.startsWith("public ") ||
                trimmed.startsWith("interface ") || trimmed.startsWith("@") ||
                trimmed.startsWith("import ") || trimmed.startsWith("package ")
            }
            val prunedText = prunedLines.joinToString("\n")
            val prunedTokens = prunedText.split(Regex("\\s+")).filter { it.isNotBlank() }.size
            val saved = (originalTokens - prunedTokens).coerceAtLeast(0)
            val ratio = if (originalTokens > 0) (saved.toDouble() / originalTokens.toDouble()) * 100.0 else 0.0

            return PsiTokenMetrics(
                originalTokens = originalTokens,
                prunedTokens = prunedTokens,
                savedTokens = saved,
                reductionPercentage = Math.round(ratio * 100.0) / 100.0,
                traversalMs = System.currentTimeMillis() - startTime
            )
        }
    }
}
