# Molecule

Source: https://docs.coreweave.com/products/wandb/ref/python/data-types/molecule

# Molecule

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/data_types/molecule.py#L28)

## Class wandb.Molecule

W\&B class for 3D Molecular data.

```python theme={"system"}
data_or_path: 'str | pathlib.Path | TextIO',
caption: 'str | None' = None, **kwargs: 'str'
```

## Args

**data\_or\_path** `str | pathlib.Path | TextIO`

Molecule can be initialized from a file name or an io object.

**caption** `str | None`

Caption associated with the molecule for display.

**kwargs** `str`

No description provided.

## Methods

### method Molecule.from\_rdkit()

```python theme={"system"}
data_or_path: 'RDKitDataType',
caption: 'str | None' = None,
convert_to_3d_and_optimize: 'bool' = True,
mmff_optimize_molecule_max_iterations: 'int' = 200
```

Convert RDKit-supported file/object types to wandb.Molecule.

##### Arguments

**data\_or\_path** `RDKitDataType`

(string, rdkit.Chem.rdchem.Mol) Molecule can be initialized from a file name or an rdkit.Chem.rdchem.Mol object.

**caption** `str | None`

(string) Caption associated with the molecule for display.

**convert\_to\_3d\_and\_optimize** `bool`

(bool) Convert to rdkit.Chem.rdchem.Mol with 3D coordinates. This is an expensive operation that may take a long time for complicated molecules.

### method Molecule.from\_smiles()

```python theme={"system"}
data: 'str',
caption: 'str | None' = None,
sanitize: 'bool' = True,
convert_to_3d_and_optimize: 'bool' = True,
mmff_optimize_molecule_max_iterations: 'int' = 200
```

Convert SMILES string to wandb.Molecule.

##### Arguments

**data** `str`

SMILES string.

**caption** `str | None`

Caption associated with the molecule for display.

**sanitize** `bool`

Check if the molecule is chemically reasonable by the RDKit's definition.

**convert\_to\_3d\_and\_optimize** `bool`

Convert to rdkit.Chem.rdchem.Mol with 3D coordinates. This is a computationally intensive operation that may take a long time for complicated molecules.
