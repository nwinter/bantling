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

allSavedNames = {liked: [], hated: []}
module.exports.loadSavedNames = loadSavedNames = ->
  onSuccess = (savedNames, textStatus, jqXHR) ->
    console.log "Loaded", savedNames.liked.length, "liked names and", savedNames.hated.length, "hated names."
    allSavedNames = savedNames
    renderSavedNames()
    loadNames()

  onError = (jqXHR, textStatus, errorThrown) ->
    console.log "Couldn't load savedNames; are you logged in?\n", jqXHR, textStatus, errorThrown

  console.log "Loading savedNames..."
  $.ajax
    dataType: "json"
    url: "/saved_names/"
    success: onSuccess
    error: onError

module.exports.saveNames = saveNames = (callback) ->
  onSuccess = (savedNames, textStatus, jqXHR) ->
    #console.log "Saved", savedNames.liked.length, "liked names and", savedNames.hated.length, "hated names."
    callback?()

  onError = (jqXHR, textStatus, errorThrown) ->
    console.log "Couldn't save names; are you logged in?\n", jqXHR, textStatus, errorThrown

  #console.log "Saving names...", allSavedNames
  $.ajax
    dataType: "json"
    url: "/saved_names/"
    success: onSuccess
    error: onError
    method: 'POST'
    data: allSavedNames

module.exports.listenToSliders = listenToSliders = ->
  $('.slider-control').on 'change', ->
    scoreID = $(@).attr('id')
    _.find(defaultScorers, scoreID: scoreID).weight = parseInt $(@).val(), 10
    renderNames()
  $('.btn-row input').on 'change', ->
    renderNames()
  $('.needs-tooltip').tooltip placement: 'bottom'

module.exports.listenToButtons = listenToButtons = ->
  $('tr .save-button').off('click').on 'click', (e) ->
    button = $(e.target).closest 'button'
    row = button.closest('tr')
    name = row.find('td:first-child').text()
    like = button.hasClass 'like-button'
    hate = button.hasClass 'hate-button'
    allSavedNames.liked = _.without allSavedNames.liked, name
    allSavedNames.hated = _.without allSavedNames.hated, name
    allSavedNames.liked.push name if like
    allSavedNames.hated.push name if hate
    row.remove()
    saveNames()
    renderSavedNames()
    if hate
      $('#saved-hated-panel:not(.in)').collapse('toggle')

renderNames = ->
  table = $('#name-list-table')
  table.find('button').off 'click'
  tbody = table.find('tbody').empty()
  for name, rank in allNames
    #console.log 'making score', judge(defaultScorers, name), 'for', name if i is 0
    name.score = judge defaultScorers, name
  allNames = _.sortBy(allNames, 'score').reverse()
  allNames = _.reject allNames, (name) -> (name.name in allSavedNames.liked) or (name.name in allSavedNames.hated)
  genders = []
  genders.push "F" if $('#gender-female').is ':checked'
  genders.push "M" if $('#gender-male').is ':checked'
  allGenderMatchNames = _.filter allNames, (name) -> _.intersection(name.genders, genders).length
  for name, rank in allGenderMatchNames
    break if rank > 100
    genders = ({F: "Female", M: "Male"}[gender] for gender in name.genders).join ", "
    row = $("<tr></tr>")
    row.append $("<td>#{name.name}</td>")
    row.append $("<td>#{Math.round(name.score)}</td>")
    row.append $("<td>#{genders}</td>")
    row.append $("<td><button class='btn btn-primary btn-xs like-button save-button'>Like</button></td>")
    row.append $("<td><button class='btn btn-warning btn-xs hate-button save-button'>Hate</button></td>")
    row.append $("<td>#{name.meaning or ''}</td>")
    tbody.append(row)
  listenToButtons()

renderSavedNames = ->
  for type in ['liked', 'hated']
    names = allSavedNames[type]
    list = $("#saved-#{type}-list").empty()
    for name in names
      li = $("<li class='list-group-item'>#{name}</li>")
      list.append li
    unless names.length
      li = $("<li class='list-group-item'>No #{type} names yet.</li>")
      list.append li
    $("#saved-#{type} .panel-title .badge").text names.length

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
  {scoreID: "history-rarity", weight: 10}
  #{scoreID: "internet-googlability", weight: 8}
  #{scoreID: "internet-availability", weight: 4}
  {scoreID: "meaning-secularity", weight: 30}
  #{scoreID: "beauty-palindromicity", weight: 20}
  #{scoreID: "beauty-initialization", weight: 1}
  {scoreID: "speed-shortness", weight: 20}
  {scoreID: "speed-recitability", weight: 4}
  {scoreID: "speed-nicklessness", weight: 15}
  {scoreID: "speed-nickedness", weight: 10}
  {scoreID: "culture-chineseness", weight: 4}
  {scoreID: "culture-genderedness", weight: 20}
]

# top names list page
module.exports.highlightNameOpinions = highlightNameOpinions = (liked, hated) ->
  $('.top-names-list-item').each ->
    name = $(@).data 'name'
    $(@).addClass 'liked' if name in liked
    $(@).addClass 'hated' if name in hated
    $(@).find('.btn-warning').prop('disabled', true) if name in hated
    $(@).find('.btn-primary').prop('disabled', true) if name in liked

module.exports.listenToTopNameButtons = listenToTopNameButtons = ->
  $('.top-names-list-item .save-button').off('click').on 'click', (e) ->
    button = $(e.target).closest 'button'
    li = button.closest('li')
    name = li.data('name')
    like = button.hasClass 'like-button'
    hate = button.hasClass 'hate-button'
    allSavedNames.liked = _.without allSavedNames.liked, name
    allSavedNames.hated = _.without allSavedNames.hated, name
    allSavedNames.liked.push name if like
    allSavedNames.hated.push name if hate
    highlightNameOpinions allSavedNames.liked, allSavedNames.hated
    saveNames()
