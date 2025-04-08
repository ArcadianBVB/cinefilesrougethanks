document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchProduct");
    const searchResults = document.getElementById("searchResults");
    const selectedProductsTable = document.querySelector("#selectedProducts tbody");
    const montantTotalField = document.getElementById("montant_total");
    const produitsJsonField = document.getElementById("produits_json");

    function recalculerTotal() {
        let totalGlobal = 0;
        const rows = selectedProductsTable.querySelectorAll("tr");
        rows.forEach(row => {
            const totalCell = row.querySelector(".total-cell");
            totalGlobal += parseFloat(totalCell.textContent);
        });
        montantTotalField.value = totalGlobal.toFixed(2);
        mettreAJourProduitsJSON();
    }

    function mettreAJourProduitsJSON() {
        let produits = [];
        const rows = selectedProductsTable.querySelectorAll("tr");
        rows.forEach(row => {
            const titre = row.querySelector(".titre-cell").textContent;
            const qualite = row.querySelector(".qualite-cell").textContent;
            const prix = parseFloat(row.querySelector(".prix-cell").textContent);
            const quantite = parseFloat(row.querySelector(".quantite-input").value);
            const total = parseFloat(row.querySelector(".total-cell").textContent);
            produits.push({ titre, qualite, prix, quantite, total });
        });
        produitsJsonField.value = JSON.stringify(produits);
    }

    window.searchProducts = function() {
        let query = searchInput.value;
        if (!query.trim()) {
            searchResults.innerHTML = "";
            return;
        }
        fetch(`/commandes/search_products?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                searchResults.innerHTML = "";
                if (data.length === 0) {
                    searchResults.innerHTML = "<p>Aucun résultat trouvé.</p>";
                } else {
                    data.forEach(product => {
                        let div = document.createElement("div");
                        div.classList.add("search-result-item");
                        div.textContent = `${product.titre} – ${product.qualite} – ${parseFloat(product.prix).toFixed(2)} $`;
                        // Au clic, on ajoute le produit au tableau avec quantité par défaut = 1
                        div.onclick = function() {
                            ajouterProduit(product);
                            searchResults.innerHTML = "";
                            searchInput.value = "";
                        };
                        searchResults.appendChild(div);
                    });
                }
            })
            .catch(err => {
                console.error("Erreur lors de la recherche :", err);
                searchResults.innerHTML = "<p>Erreur lors de la recherche.</p>";
            });
    };

    function ajouterProduit(product) {
        let row = document.createElement("tr");

        let titreCell = document.createElement("td");
        titreCell.className = "titre-cell";
        titreCell.textContent = product.titre;

        let qualiteCell = document.createElement("td");
        qualiteCell.className = "qualite-cell";
        qualiteCell.textContent = product.qualite;

        let prixCell = document.createElement("td");
        prixCell.className = "prix-cell";
        prixCell.textContent = parseFloat(product.prix).toFixed(2);

        let quantiteCell = document.createElement("td");
        let quantiteInput = document.createElement("input");
        quantiteInput.type = "number";
        quantiteInput.value = 1;
        quantiteInput.min = 1;
        quantiteInput.classList.add("quantite-input");
        quantiteInput.onchange = function() {
            majTotalLigne(row);
        };
        quantiteCell.appendChild(quantiteInput);

        let totalCell = document.createElement("td");
        totalCell.className = "total-cell";
        totalCell.textContent = parseFloat(product.prix).toFixed(2);

        let supprCell = document.createElement("td");
        let supprBtn = document.createElement("button");
        supprBtn.textContent = "X";
        supprBtn.onclick = function() {
            row.remove();
            recalculerTotal();
        };
        supprCell.appendChild(supprBtn);

        row.appendChild(titreCell);
        row.appendChild(qualiteCell);
        row.appendChild(prixCell);
        row.appendChild(quantiteCell);
        row.appendChild(totalCell);
        row.appendChild(supprCell);

        selectedProductsTable.appendChild(row);
        recalculerTotal();
    }

    function majTotalLigne(row) {
        let prix = parseFloat(row.querySelector(".prix-cell").textContent);
        let quantite = parseFloat(row.querySelector(".quantite-input").value);
        let totalCell = row.querySelector(".total-cell");
        totalCell.textContent = (prix * quantite).toFixed(2);
        recalculerTotal();
    }
});
