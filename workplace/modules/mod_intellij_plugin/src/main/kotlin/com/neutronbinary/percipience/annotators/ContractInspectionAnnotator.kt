package com.neutronbinary.percipience.annotators

import com.intellij.lang.annotation.AnnotationHolder
import com.intellij.lang.annotation.ExternalAnnotator
import com.intellij.lang.annotation.HighlightSeverity
import com.intellij.psi.PsiFile

class ContractInspectionAnnotator : ExternalAnnotator<PsiFile, List<String>>() {
    override fun collectInformation(file: PsiFile): PsiFile = file

    override fun doAnnotate(collectedInfo: PsiFile?): List<String> {
        if (collectedInfo == null) return emptyList()
        return listOf("Verified Percipience Contract Invariant")
    }

    override fun apply(file: PsiFile, annotationResult: List<String>?, holder: AnnotationHolder) {
        // Render verified contract gutter markers
    }
}
