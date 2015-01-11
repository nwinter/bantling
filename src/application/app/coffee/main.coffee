Utils =
  renderFieldErrorTooltip: (selector, msg, placement="right") ->
    placement ?= "right"  if typeof placement is "undefined"  # default to right-aligned tooltip
    elem = $(selector)
    elem.tooltip
      title: msg
      trigger: "manual"
      placement: placement

    elem.tooltip "show"
    elem.addClass "error"
    elem.on "focus click", (e) ->
      elem.removeClass "error"
      elem.tooltip "hide"
      return

allNames = []
module.exports.loadNames = loadNames = ->
  onSuccess = (names, textStatus, jqXHR) ->
    console.log "Loaded", names.length, "names."
    allNames = names
    renderNames()

  onError = (jqXHR, textStatus, errorThrown) ->
    console.log "Couldn't load names; have you generated them with the script? python scripts/bantling.py\n", jqXHR, textStatus, errorThrown

  console.log "Loading names..."
  $.ajax
    dataType: "json"
    url: "/static/js/names.json"
    success: onSuccess
    error: onError
  return

module.exports.listenToSliders = listenToSliders = ->
  $('.slider-control').on 'change', ->
    scoreID = $(@).attr('id')
    _.find(defaultScorers, scoreID: scoreID).weight = parseInt $(@).val(), 10
    renderNames()
  $('.btn-row input').on 'change', ->
    renderNames()

renderNames = ->
  table = $('#name-list-table')
  tbody = table.find('tbody').empty()
  for name in allNames
    name.score = judge defaultScorers, name
  allNames = _.sortBy(allNames, 'score').reverse()
  genders = []
  genders.push "F" if $('#gender-female').is ':checked'
  genders.push "M" if $('#gender-male').is ':checked'
  console.log 'genders', genders
  allGenderMatchNames = _.filter allNames, (name) -> _.intersection(name.genders, genders).length
  for name, rank in allGenderMatchNames
    break if rank > 100
    genders = ({F: "Female", M: "Male"}[gender] for gender in name.genders).join ", "
    row = $("<tr></tr>")
    row.append $("<td>#{name.name}</td>")
    row.append $("<td>#{Math.round(name.score)}</td>")
    row.append $("<td>#{genders}</td>")
    row.append $("<td><a href='' class='btn'>Like</a></td>")
    row.append $("<td><a href='' class='btn'>Hate</a></td>")
    tbody.append(row)

module.exports.judge = judge = (scorers, name) ->
  scorers ?= defaultScorers
  totalWeight = 0
  score = 0
  for scorer in scorers
    totalWeight += scorer.weight
    score += name.scores[scorer.scoreID] * scorer.weight
  100 * score / totalWeight

defaultScorers = [
  {scoreID: "phonetics-spellability", weight: 40}
  {scoreID: "phonetics-pronounceability", weight: 10}
  {scoreID: "history-timelessness", weight: 20}
  {scoreID: "history-relevancy", weight: 30}
  {scoreID: "history-rarity", weight: 30}
  {scoreID: "internet-googlability", weight: 8}
  {scoreID: "internet-availability", weight: 4}
  {scoreID: "meaning-secularity", weight: 30}
  {scoreID: "meaning-seriousness", weight: 3}
  {scoreID: "beauty-palindromicity", weight: 5}
  {scoreID: "beauty-initialization", weight: 10}
  {scoreID: "speed-shortness", weight: 20}
  {scoreID: "speed-recitability", weight: 4}
  {scoreID: "speed-nicklessness", weight: 15}
  {scoreID: "culture-chineseness", weight: 4}
  {scoreID: "culture-genderedness", weight: 20}
]
