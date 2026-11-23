# Model Architecture Benchmarks & Performance Comparison

| Model | Target Disease | Parameters | Forward Pass Latency (CPU) | Input Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **ResNet-50** | Anemia ($Hb$ regression) | 25.6 M | ~48 ms | 224 × 224 |
| **MobileNetV3-Small** | SLID Conjunctival Injection | 2.5 M | ~12 ms | 224 × 224 |
| **MobileNetV3-Small** | Scleral Icterus (Jaundice) | 2.5 M | ~11 ms | 224 × 224 |
| **ResNet-18** | Nuclear Cataract | 11.7 M | ~24 ms | 224 × 224 |

MobileNetV3 provides a 4x latency advantage on low-power Intel and ARM processors.
