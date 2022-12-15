$(document).ready(function ($) {
    $('#autoComplete').on('keyup', function(e){
        if(e.which === 13) {
            window.open(`/anime?search=${document.getElementById('autoComplete').value}`, "_self")
        }
    });
});

const autoCompleteJS = new autoComplete({
    placeHolder: "Поиск аниме...",
    data: {
        src: async () => {
            const source = await fetch(
                `/anime?search=${document.getElementById('autoComplete').value}`
            ).then(function(responce) {
                return responce.text();
            });
            const data = await source;

            var suggestions = Array.from($(data).find('#item-list a')).map(function (item) {
                return item.innerHTML;
            });

            return await suggestions;
        },
    },
    resultItem: {
        highlight: true
    },
    threshold: 2,
    searchEngine: "strict",
    events: {
        input: {
            selection: (event) => {
                const selection = event.detail.selection.value;
                autoCompleteJS.input.value = selection;
            }
        }
    }
});

