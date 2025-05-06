from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all submodules
hiddenimports = collect_submodules('matplotlib')

# Collect all data files
datas = collect_data_files('matplotlib')

# Add specific matplotlib backends
hiddenimports += [
    'matplotlib.backends.backend_tkagg',
    'matplotlib.backends.backend_svg',
    'matplotlib.backends.backend_pdf',
    'matplotlib.backends.backend_ps',
    'matplotlib.backends.backend_template',
] 