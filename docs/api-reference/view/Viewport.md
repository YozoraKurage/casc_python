# csc.view.Viewport

> 公式: https://cascadeur.com/python-api/_generate/csc.view.Viewport.html

`class csc.view.Viewport`

Viewport class

```python
import csc
def run(scene):
    application = csc.app.get_application()
    cs = application.current_scene()
    active_viewport = cs.active_viewport().domain_viewport()
    print(f"Active viewport: {active_viewport.id}")
```

## Methods

- `__init__(*args, **kwargs)`
- `domain_viewport(self: csc.view.Viewport) -> object`
  - Get the domain viewport.
  - Returns: The domain viewport.
  - Return type: csc.view.ViewportDomain
- `selectable_types(self: csc.view.Viewport) -> set[str]`
  - Get selectable types for current viewport mode.
  - Returns: The selectable types.
  - Return type: set(str)
