const fileJson = 'journal.json';
const urlBase = 'http://localhost:1407/cgi-bin/journal/journal-new.py';

debbyPlay.tagList =[];
debbyPlay.placeList =[];
debbyPlay.peopleList =[];
debbyPlay.days =[];

function initJournal(){
	for (var d in debbyPlay.days){
		if (! containsList (debbyPlay.placeList, debbyPlay.days[d].place) && debbyPlay.days[d].place)
			debbyPlay.placeList.push (debbyPlay.days[d].place);
		for (var t in debbyPlay.days[d].tags){
			if (! containsList (debbyPlay.tagList, debbyPlay.days[d].tags[t]))
				debbyPlay.tagList.push (debbyPlay.days[d].tags[t]);
		}
		for (var t in debbyPlay.days[d].peoples){
			if (! containsList (debbyPlay.peopleList, debbyPlay.days[d].peoples[t]))
				debbyPlay.peopleList.push (debbyPlay.days[d].peoples[t]);
	}}
	debbyPlay.placeList.sort();
	debbyPlay.peopleList.sort();
	debbyPlay.tagList.sort();
	debbyPlay.placeCurrent ="";
	debbyPlay.peoplesCurrent ="";
	debbyPlay.tagsCurrent ="";
}
function register(){
	if (! document.getElementById ('date') || ! document.getElementById ('place')){
		document.getElementById ('response').innerHTML = '<p>il manque la date ou le lieu</p>';
		document.getElementById ('response').className = 'error';
	}
	else{
		var message = document.getElementById ('message').value.replace ('\n', ' $ ');
		var params = '?place=' + document.getElementById ('place').value + '&date=' + document.getElementById ('date').value
			+ '&peoples=' + document.getElementById ('peoples').value + '&tags=' + document.getElementById ('tags').value
			+ '&title=' + document.getElementById ('title').value + '&message=' + message;
		var url = urlBase + params;
		var xhttp = new XMLHttpRequest();
		xhttp.open ('GET', url, false);
		xhttp.send();
		if (xhttp.status ==200){
			if (xhttp.responseText.contain ('</'))
				document.getElementById ('response').innerHTML = "<p>une erreur empêche l'enregistrement de l'article</p>" + xhttp.responseText;
			else{
				var resultatJson = JSON.parse (xhttp.responseText);
				console.log (resultatJson);
				document.getElementById ('response').innerHTML = "<p>l'article a été enregistré avec succès</p>";
			}
			document.getElementById ('response').className = 'error';
		}
	}
}
function containsList (list, word){
	if (list.indexOf (word) >-1) return true;
	else return false;
}
document.body.init();
debbyPlay.days = useJson (fileJson);
initJournal();
function selectPlace (place){
	debbyPlay.placeCurrent = place.toLowerCase();
	document.getElementById ('place').load();
}
function selectPeoples (people){
	debbyPlay.peoplesCurrent = debbyPlay.peoplesCurrent +', '+ people.toLowerCase();
	if (debbyPlay.peoplesCurrent.slice (0,2) ==', ') debbyPlay.peoplesCurrent = debbyPlay.peoplesCurrent.slice (2);
	document.getElementById ('peoples').load();
}
function selectTags (tag){
	debbyPlay.tagsCurrent = debbyPlay.tagsCurrent +', '+ tag.toLowerCase();
	if (debbyPlay.tagsCurrent.slice (0,2) ==', ') debbyPlay.tagsCurrent = debbyPlay.tagsCurrent.slice (2);
//	document.getElementById ('tags').value = debbyPlay.tagsCurrent;
	document.getElementById ('tags').load();
}
document.body.load();
