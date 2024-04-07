# PBW Cara7
Dans le cadre de la Paris Blockchain Week, nous avons conçu une preuve de concept (PoC) pour un service de titrisation exploitant la blockchain XRP.

## Problématique :

Les sociétés de financement des constructeurs automobiles cèdent les contrats de financement à des fonds de pension. Ces derniers nécessitent des données financières détaillées, impliquant de nombreuses heures d'analyse par des experts et un volume limité de données disponibles.

Ce projet vise à optimiser la titrisation des contrats de leasing automobile, en assurant une transparence accrue concernant la santé financière des leasing et l'état des véhicules.

Une meilleure information dans ce domaine favorisera une maturité accrue des leasing et contribuera à une démocratisation plus importante des voitures électriques.

## Fonctionnement technique :

### Création du NFT et smartcontract sur EVM

Lorsque la voiture est vendue, un jeton non fongible (NFT) est créé sur la blockchain XRP. Ce NFT contient l'adresse d'un contrat intelligent situé sur l'EVM (Ethereum Virtual Machine), lequel conserve une collection de hachages de fichiers historiques représentant l'état passé de la voiture ainsi que sa santé financière.
