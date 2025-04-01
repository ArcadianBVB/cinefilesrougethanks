document.addEventListener("DOMContentLoaded", function () {
    const typeField = document.getElementById("type");
    const formatField = document.getElementById("format");
    const qualiteField = document.getElementById("qualite");
    const rareteField = document.getElementById("rarete");
    const saisonField = document.getElementById("saison");
    const episodesField = document.getElementById("episodes");
    const prixField = document.getElementById("prix");

    function miseAJourPrix() {
        const data = {
            type: typeField.value,
            format: formatField.value,
            qualite: qualiteField.value,
            rarete: rareteField.value,
            saison: saisonField.value,
            episodes: episodesField.value
        };

        fetch("/prix_auto", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(result => {
            prixField.value = result.prix;
        })
        .catch(err => console.error("Erreur dans le calcul du prix :", err));
    }

    [typeField, formatField, qualiteField, rareteField, saisonField, episodesField].forEach(el => {
        el.addEventListener("change", miseAJourPrix);
    });

    miseAJourPrix();
});
