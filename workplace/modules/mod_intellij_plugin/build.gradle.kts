plugins {
    id("java")
    id("org.jetbrains.kotlin.jvm") version "2.0.0"
    id("org.jetbrains.intellij.platform") version "2.0.1"
}

group = "com.neutronbinary.percipience"
version = "1.0.0"

repositories {
    mavenCentral()
    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        intellijIdeaCommunity("2024.2.1")
        bundledPlugins("com.intellij.java", "org.jetbrains.kotlin")
        pluginVerifier()
        zipSigner()
    }
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.1")
}

intellijPlatform {
    pluginConfiguration {
        id = "com.neutronbinary.percipience"
        name = "Percipience Context Engineering OS"
        version = "1.0.0"
        vendor {
            name = "Neutron Binary"
            url = "https://percipience.dev"
        }
        ideaVersion {
            sinceBuild = "241.0"
            untilBuild = "262.*"
        }
    }
}
