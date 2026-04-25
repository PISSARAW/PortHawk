# PortHawk

> **Avertissement legal et ethique**
>
> PortHawk est un outil educatif. Vous devez scanner uniquement des hotes
> que vous possedez ou pour lesquels vous avez une autorisation explicite.
>
> Le scan non autorise peut etre illegal selon votre juridiction.
> Les auteurs ne sont pas responsables d'un usage malveillant ou illicite.

PortHawk est un scanner TCP en Python (bibliotheque standard) qui permet de:

- scanner des ports en mode sequentiel ou multi-threads
- gerer un timeout par port
- afficher un resume lisible dans le terminal
- exporter les resultats en JSON et CSV
- journaliser l'execution (stderr et fichier optionnel)

## Etat actuel du projet

- CLI fonctionnelle via `python -m porthawk` et `porthawk`
- Parse de ports supporte: `22,80,443`, `1-1024`, combinaisons dedoublonnees et triees
- Scan TCP connect implemente dans `porthawk/scanner.py`
- Export JSON/CSV implemente dans `porthawk/output.py`
- Logging centralise implemente dans `porthawk/logger.py`
- Module `porthawk/banner.py` encore non implemente (`NotImplementedError`)

Resultat des tests actuel:

- `29 passed, 10 skipped`

## Installation

Prerequis:

- Python `>= 3.10`

Installation locale:

```bash
git clone https://github.com/PISSARAW/PortHawk.git
cd PortHawk
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Utilisation

### Commande minimale

```bash
python -m porthawk 127.0.0.1
```

### Exemples

```bash
# Scan d'une plage de ports
python -m porthawk 127.0.0.1 --ports 1-1024

# Scan de ports cibles avec threads
python -m porthawk 192.168.1.10 --ports 22,80,443 --threads --max-workers 200

# Export des resultats
python -m porthawk 10.0.0.5 --ports 1-1000 --output-json results.json --output-csv results.csv

# Affichage detaille de tous les ports scannes
python -m porthawk 127.0.0.1 --ports 1-20 --show-all
```

### Options CLI

- `host` (positionnel): nom d'hote ou adresse IP cible
- `--ports`: liste/plage de ports (defaut `1-1024`)
- `--timeout`: timeout par port en secondes (defaut `1.0`)
- `--threads`: active le scan multi-threads
- `--max-workers`: nombre max de workers si `--threads` (defaut `100`)
- `--output-json`: chemin de sortie JSON
- `--output-csv`: chemin de sortie CSV
- `--log-file`: fichier de log optionnel
- `--verbose`: active les logs DEBUG
- `--show-all`: affiche un tableau complet (ports ouverts + fermes + filtres)

## Format des resultats

Chaque resultat de scan suit ce schema:

```json
{
	"port": 22,
	"state": "open",
	"banner": "SSH-2.0-OpenSSH_9.0"
}
```

Valeurs possibles pour `state`:

- `open`
- `closed`
- `filtered`

## Lancer les tests

```bash
pytest -q
```

## Structure du projet

```text
PortHawk/
|- porthawk/
|  |- __main__.py
|  |- scanner.py
|  |- output.py
|  |- logger.py
|  |- banner.py
|- tests/
|- pyproject.toml
|- requirements.txt
|- README.md
```

## Roadmap courte

- implementer `grab_banner()` dans `porthawk/banner.py`
- ajouter des tests d'integration reseau plus complets
- enrichir les sorties (timestamps, metadonnees de scan)

## Licence

Projet distribue sous licence [MIT](LICENSE).
