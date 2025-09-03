
@ECHO OFF

set SPHINXBUILD=sphinx-build
set SOURCEDIR=source
set BUILDDIR=_build

if "%1"=="" (
    %SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR%
) else (
    %SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR%
)
