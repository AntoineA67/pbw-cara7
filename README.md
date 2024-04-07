![](/img/1.png)

# PBW Cara7
Dans le cadre de la Paris Blockchain Week, nous avons conçu une preuve de concept (PoC) pour un service de titrisation exploitant la blockchain XRP.

## Problématique :

Les sociétés de financement des constructeurs automobiles cèdent les contrats de financement à des fonds de pension. Ces derniers nécessitent des données financières détaillées, impliquant de nombreuses heures d'analyse par des experts et un volume limité de données disponibles.

Ce projet vise à optimiser la titrisation des contrats de leasing automobile, en assurant une transparence accrue concernant la santé financière des leasing et l'état des véhicules.

Une meilleure information dans ce domaine favorisera une maturité accrue des leasing et contribuera à une démocratisation plus importante des voitures électriques.

## Fonctionnement technique :

#### Création du NFT et smartcontract sur EVM

Lorsque la voiture est vendue, [un jeton non fongible (NFT)](https://github.com/AntoineA67/pbw-cara7/blob/main/script/1_Create.py) est créé sur la blockchain XRP. Ce NFT contient [https://github.com/AntoineA67/pbw-cara7/blob/main/evm-interaction/contracts/HashStorage.sol](l'adresse d'un contrat intelligent situé sur l'EVM)  (Ethereum Virtual Machine), lequel conserve une collection de hachages de fichiers historiques représentant l'état passé de la voiture ainsi que sa santé financière.

[![](/img/2.png)](https://miro.com/app/board/uXjVKXynQg8=/?moveToViewport=-2594,1316,2684,1234&embedId=215828249926)

#### Mise à jour des informations techniques et financière

Périodiquement, les données techniques et financières sont transmises à une [agrégation de données](https://github.com/AntoineA67/pbw-cara7/blob/main/script/2_Update.py), puis elles sont enregistrées dans un fichier JSON. Ensuite, un hachage de ce fichier est généré et stocké dans un contrat intelligent sur l'EVM (Ethereum Virtual Machine) d'XRP. Ce contrat intelligent permet de récupérer tous les hachages qui y ont été ajoutés et d'ajouter de nouveaux hachages, sans possibilité de modifier les hachages déjà existants.

[![](/img/3.png)](https://miro.com/app/live-embed/uXjVKXynQg8=/?moveToViewport=-2250,2617,2189,1006&embedId=328669422631)

#### Analyse financière et trunching en plusieurs profiles de risques

Après une certaine durée de vie du véhicule, un processus de trunching est déclenché en fonction de l'évaluation du risque technique du véhicule ainsi que des capacités de remboursement actuelles et futures de l'acheteur, afin de classifier le niveau de risque. Dans notre cas, nous classons les véhicules représentés par des NFT dans trois portefeuilles distincts, chacun représentant des niveaux de risque différents.

Les NFT sont destinés à être associés à ces différents portefeuilles afin d'être acquis tant par des fonds d'investissement désireux de prendre en charge le risque jusqu'à la fin de la maturité du leasing que par des particuliers qui peuvent investir dans cet actif via un échange décentralisé (DEX).

[![](/img/4.png)](https://miro.com/app/live-embed/uXjVKXynQg8=/?moveToViewport=-2387,3742,2624,1207&embedId=338572393257)

[![](/img/5.png)](https://miro.com/app/live-embed/uXjVKXynQg8=/?moveToViewport=-2736,5242,4017,1847&embedId=56264919248)

## Interface graphique :

.image.
