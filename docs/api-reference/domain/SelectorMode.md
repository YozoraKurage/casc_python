# csc.domain.SelectorMode

> 公式: https://cascadeur.com/python-api/_generate/csc.domain.SelectorMode.html

`class csc.domain.SelectorMode`

SelectorMode enumerable

SingleSelection, // Resets if new objects were selected, and nothing changes if already selected ones were selected

MultiSelection, // Multiple selections. If not all objects were selected, adds, otherwise subtracts

NewSelection, // Resets everything and highlights the selection

AdditionSelection, // Adds all selections to selections

SubtractionSelection // Subtracts highlighted entities from selections

## Members

- `SingleSelection` = 0
- `MultiSelection` = 1
- `NewSelection` = 2
- `AdditionSelection` = 3
- `SubtractionSelection` = 4
