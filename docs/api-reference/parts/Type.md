# csc.parts.Type

> 公式: https://cascadeur.com/python-api/_generate/csc.parts.Type.html

Type of the parts, enum

## Members

- `Elementary` = 0
- `UpdateGroup` = 1
- `Object` = 2
- `ObjectGroup` = 3
- `SelectedObjects` = 4

## Description

- **Elementary**: includes only regular and setting functions + regular and setting data + connections that link them
- **UpdateGroup**: sub update groups and their elementary entities + connections that link them
- **Object**: includes all related entities of some object
- **ObjectGroup**: includes all objects and sub object groups and all related entities
- **SelectedObjects**: selected objects from different groups

## Methods

- `__init__(self: csc.parts.Type, value: int) → None`
- `__eq__(self: object, other: object) → bool`
- `__getstate__(self: object) → int`
- `__hash__(self: object) → int`
- `__index__(self: csc.parts.Type) → int`
- `__int__(self: csc.parts.Type) → int`
- `__ne__(self: object, other: object) → bool`
- `__repr__(self: object) → str`
- `__setstate__(self: csc.parts.Type, state: int) → None`
- `__str__(self: object) → str`

## Properties

- `name`: property
- `value`: property
