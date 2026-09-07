#let titleblock(title, subtitle) = [
  #align(center)[
    #text(size: 24pt, weight: "bold")[#title]
    #v(4pt)
    #text(size: 13pt)[#subtitle]
  ]
]

#titleblock(
  "SoupDB: Minigestor de Base de Datos Multimodal",
  "Informe técnico · Base de Datos 2 · UTEC · ciclo 2026-2",
)

= Resumen

#lorem(60)

= Introducción

#lorem(80)

= Arquitectura

#lorem(80)

= Almacenamiento y organización de archivos

#lorem(80)

= Indexación y optimización

#lorem(80)

= Procesamiento de consultas SQL

#lorem(80)

= Transacciones y concurrencia

#lorem(80)

= Benchmarks

#lorem(80)

= Conclusiones

#lorem(60)

#bibliography("refs.bib")