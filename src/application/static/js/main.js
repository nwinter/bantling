var Utils = {
    renderFieldErrorTooltip: function (selector, msg, placement) {
        var elem;
        if (typeof placement === 'undefined') {
            placement = 'right'; // default to right-aligned tooltip
        }
        elem = $(selector);
        elem.tooltip({'title': msg, 'trigger': 'manual', 'placement': placement});
        elem.tooltip('show');
        elem.addClass('error');
        elem.on('focus click', function(e) {
            elem.removeClass('error');
            elem.tooltip('hide');
        });
    }
};

/* Your custom JavaScript here */

var defaultWeights = [
    {scoreID: "phonetics.spellability", weight: 40},
    {scoreID: "phonetics.pronounceability", weight: 10},
    {scoreID: "history.timelessness", weight: 20},
    {scoreID: "history.relevancy", weight: 30},
    {scoreID: "history.rarity", weight: 30},
    {scoreID: "internet.googlability", weight: 8},
    {scoreID: "internet.availability", weight: 4},
    {scoreID: "meaning.secularity", weight: 30},
    {scoreID: "meaning.seriousness", weight: 3},
    {scoreID: "beauty.palindromicity", weight: 5},
    {scoreID: "beauty.initialization", weight: 10},
    {scoreID: "speed.shortness", weight: 20},
    {scoreID: "speed.recitability", weight: 4},
    {scoreID: "speed.nicklessness", weight: 15},
    {scoreID: "culture.chineseness", weight: 4},
    {scoreID: "culture.genderedness", weight: 20},
    {scoreID: "speed.nicklessness", weight: 15}
];

function judge(weights, name) {
  weights = weights || defaultWeights;
  var totalWeight = 0;
  var score = 0;
  for (var i = 0; i < weights.length; ++i) {
    var weight = weights[i].weight;
    totalWeight += weight;
    score += name.scores[weights[i].scoreID] * weight;
  }
  return 100 * score / totalWeight;
}

function loadNames() {
  var onSuccess = function(names, textStatus, jqXHR) {
    console.log('Loaded', names.length, 'names.');
  };
  var onError = function(jqXHR, textStatus, errorThrown) {
    console.log("Couldn't load names; have you generated them with the script? python scripts/bantling.py\n", jqXHR, textStatus, errorThrown);
  };
  console.log("Loading names...");
  $.ajax({dataType: 'json', url: '/static/js/names.json', success: onSuccess, error: onError});
}
