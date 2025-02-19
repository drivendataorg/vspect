## vspect

**Functions:**

- [**format_version**](#vspect.format_version) – Format a version using a format string.
- [**get_package_version**](#vspect.get_package_version) – Get the version of a package.
- [**read_version_from_pyproject_toml**](#vspect.read_version_from_pyproject_toml) – Read the version from a pyproject.toml file. Requires the version to be statically defined.

### vspect.format_version

```python
format_version(version, format_string)
```

Format a version using a format string.

**Parameters:**

- **version** (<code>[Version](#packaging.version.Version)</code>) – The version to format.
- **format_string** (<code>[str](#str)</code>) – The format string to use.

**Returns:**

- <code>[str](#str)</code> – (str: The formatted version).

### vspect.get_package_version

```python
get_package_version(package_name)
```

Get the version of a package.

**Parameters:**

- **package_name** (<code>[str](#str)</code>) – The name of the package to get the version of.

**Returns:**

- <code>[Version](#packaging.version.Version)</code> – The version of the package.

### vspect.read_version_from_pyproject_toml

```python
read_version_from_pyproject_toml(path)
```

Read the version from a pyproject.toml file. Requires the version to be statically defined.

**Parameters:**

- **path** (<code>[Path](#pathlib.Path)</code>) – The path to the pyproject.toml file, or the directory containing it.

**Returns:**

- <code>[Version](#packaging.version.Version)</code> – The version read from the file.
