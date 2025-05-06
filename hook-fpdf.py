from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all submodules
hiddenimports = collect_submodules('fpdf')

# Collect all data files
datas = collect_data_files('fpdf') 