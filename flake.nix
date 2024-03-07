{
  description = "A basic flake with a shell";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { nixpkgs, flake-utils, ... }:
    #flake-utils.lib.eachDefaultSystem (system:
      let
        system = "aarch64-darwin";
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python312;
        pythonPackages = pkgs.python312Packages;
        dependencies = with pythonPackages; [ pip build setuptools ];
      in
      {
        devShells.${system}.default = pkgs.mkShell {
          packages = with pkgs; [
            zsh
            python
            pythonPackages.pytest
            pythonPackages.pip
          ] ++ dependencies;
        };
        defaultPackage.${system} = pythonPackages.buildPythonPackage {
          pname = "inject-secrets";
          src = ./.;
          version = "0.0.1";
          format = "pyproject";
          propagatedBuildInputs = dependencies;
        };
      };
    #);
}
