package com.neutronbinary.percipience.actions

import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.actionSystem.CommonDataKeys
import com.intellij.openapi.ui.Messages
import com.neutronbinary.percipience.psi.PsiAstBridge

class InspectAstPruningAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val psiFile = e.getData(CommonDataKeys.PSI_FILE) ?: return
        val metrics = PsiAstBridge.extractSymbolsAndPrune(psiFile)
        Messages.showInfoMessage(
            "AST Pruning Metrics:\n" +
            "Original Tokens: ${metrics.originalTokens}\n" +
            "Pruned Tokens: ${metrics.prunedTokens}\n" +
            "Reduction: ${metrics.reductionPercentage}%\n" +
            "Traversal Time: ${metrics.traversalMs}ms",
            "Percipience AST Token Inspection"
        )
    }
}
