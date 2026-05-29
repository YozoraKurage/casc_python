# csc.layers.ItemVariant

> 公式: https://cascadeur.com/python-api/_generate/csc.layers.ItemVariant.html

`class csc.layers.ItemVariant`

ItemVariant class

Can implement a folder or layer for a header

## Methods

- `folder(self: csc.layers.ItemVariant) -> domain::scene::layers::Folder`
  - -> Folder (if it has folder otherwise none)
- `header(self: csc.layers.ItemVariant) -> csc.layers.Header`
  - -> Header
- `is_folder(self: csc.layers.ItemVariant) -> bool`
- `is_layer(self: csc.layers.ItemVariant) -> bool`
- `layer(self: csc.layers.ItemVariant) -> domain::scene::layers::Layer`
  - -> Layer (if it has layer otherwise none)
