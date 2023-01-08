const fileJson = 'journal.json';
debbyPlay.tagList =[];
debbyPlay.placeList =[];
debbyPlay.peopleList =[];
debbyPlay.years =[ 'tous', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020' ];
debbyPlay.days =[];
var allDays =[];
var yearCurrent = 'tous';
var placeCurrent = 'tous';
var tagCurrent = 'tous';
var peopleCurent = 'tous';

function initJournal(){
	for (var d in debbyPlay.days){
		allDays.push (debbyPlay.days[d]);
		if (! containsList (debbyPlay.placeList, debbyPlay.days[d].place) && debbyPlay.days[d].place)
			debbyPlay.placeList.push (debbyPlay.days[d].place);
		for (var t in debbyPlay.days[d].tags){
			if (! containsList (debbyPlay.tagList, debbyPlay.days[d].tags[t])){
				debbyPlay.tagList.push (debbyPlay.days[d].tags[t]);
		}}
		for (var t in debbyPlay.days[d].peoples){
			if (! containsList (debbyPlay.peopleList, debbyPlay.days[d].peoples[t])){
				debbyPlay.peopleList.push (debbyPlay.days[d].peoples[t]);
	}}}
	debbyPlay.placeList.sort();
	debbyPlay.placeList.unshift ('tous');
	debbyPlay.peopleList.sort();
	debbyPlay.peopleList.unshift ('tous');
	debbyPlay.tagList.sort();
	debbyPlay.tagList.unshift ('tous');
	/*
	console.log ('lieux:', debbyPlay.placeList);
	console.log ('personnes:', debbyPlay.peopleList);
	console.log ('tags:', debbyPlay.tagList);
	console.log ('jours:', debbyPlay.days);
	*/
}
function containsList (list, word){
	if (list.indexOf (word) >-1) return true;
	else return false;
}
document.body.init();
debbyPlay.days = useJson (fileJson);
debbyPlay.days.shift();
initJournal();
document.body.load();
addSubTitles();

function selectYears (year){ yearCurrent = year; }
function selectPlaces (place){ placeCurrent = place.toLowerCase(); }
function selectPeoples (people){ peopleCurent = people.toLowerCase(); }
function selectTags (tag){ tagCurrent = tag.toLowerCase(); }
function selectDays(){
	debbyPlay.days =[];
	if (yearCurrent == 'tous' && placeCurrent == 'tous' && peopleCurent == 'tous' && tagCurrent == 'tous')
		for (var j in allDays) debbyPlay.days.push (allDays[j]);
	// sélection sur un seul élément sur les quatre
	else if (yearCurrent == 'tous' && placeCurrent == 'tous' && peopleCurent == 'tous'){
		for (var j in allDays){
			if (containsList (allDays[j].tags, tagCurrent)) debbyPlay.days.push (allDays[j]);
	}}
	else if (yearCurrent == 'tous' && tagCurrent == 'tous' && peopleCurent == 'tous'){
		for (var j in allDays){
			if (allDays[j].place == placeCurrent) debbyPlay.days.push (allDays[j]);
	}}
	else if (placeCurrent == 'tous' && tagCurrent == 'tous' && peopleCurent == 'tous'){
		for (var j in allDays){
			if (allDays[j].date.contain (yearCurrent +'/')) debbyPlay.days.push (allDays[j]);
	}}
	else if (yearCurrent == 'tous' && placeCurrent == 'tous' && tagCurrent == 'tous'){
		for (var j in allDays){
			if (containsList (allDays[j].peoples, peopleCurent)) debbyPlay.days.push (allDays[j]);
	}}
	// sélection sur deux éléments
	else if (yearCurrent == 'tous' && placeCurrent == 'tous'){
		for (var j in allDays){
			if (containsList (allDays[j].tags, tagCurrent) && containsList (allDays[j].peoples, peopleCurent))
				debbyPlay.days.push (allDays[j]);
	}}
	else if (yearCurrent == 'tous' && tagCurrent == 'tous'){
		for (var j in allDays){
			if (allDays[j].place == placeCurrent && containsList (allDays[j].peoples, peopleCurent))
				debbyPlay.days.push (allDays[j]);
	}}
	else if (yearCurrent == 'tous' && peopleCurent == 'tous'){
		for (var j in allDays){
			if (allDays[j].place == placeCurrent && containsList (allDays[j].tags, tagCurrent))
				debbyPlay.days.push (allDays[j]);
	}}
	else if (tagCurrent == 'tous' && placeCurrent == 'tous'){
		for (var j in allDays){
			if (allDays[j].date.contain (yearCurrent +'/') && containsList (allDays[j].peoples, peopleCurent))
				debbyPlay.days.push (allDays[j]);
	}}
	else if (tagCurrent == 'tous' && peopleCurent == 'tous'){
		for (var j in allDays){
			if (allDays[j].date.contain (yearCurrent +'/') && allDays[j].place == placeCurrent)
				debbyPlay.days.push (allDays[j]);
	}}
	else if (placeCurrent == 'tous' && peopleCurent == 'tous'){
		for (var j in allDays){
			if (allDays[j].date.contain (yearCurrent +'/') && containsList (allDays[j].tags, tagCurrent))
				debbyPlay.days.push (allDays[j]);
	}}
	// sélection sur trois éléments
	else if (placeCurrent == 'tous'){
		for (var j in allDays){
			if (allDays[j].date.contain (yearCurrent +'/') && containsList (allDays[j].tags, tagCurrent)
				&& containsList (allDays[j].peoples, peopleCurent)) debbyPlay.days.push (allDays[j]);
	}}
	else if (yearCurrent == 'tous'){
		for (var j in allDays){
			if (allDays[j].place == placeCurrent && containsList (allDays[j].tags, tagCurrent)
				&& containsList (allDays[j].peoples, peopleCurent)) debbyPlay.days.push (allDays[j]);
	}}
	else if (peopleCurent == 'tous'){
		for (var j in allDays){
			if (allDays[j].date.contain (yearCurrent +'/') && containsList (allDays[j].tags, tagCurrent)
				&& allDays[j].place == placeCurrent) debbyPlay.days.push (allDays[j]);
	}}
	else if (tagCurrent == 'tous'){
		for (var j in allDays){
			if (allDays[j].date.contain (yearCurrent +'/') && containsList (allDays[j].peoples, peopleCurent)
				&& allDays[j].place == placeCurrent) debbyPlay.days.push (allDays[j]);
	}}
	// sélection sur tous les éléments
	else{
		for (var j in allDays){
			if (allDays[j].date.contain (yearCurrent +'/') && allDays[j].place == placeCurrent && containsList (allDays[j].tags, tagCurrent) && containsList (allDays[j].peoples, peopleCurent)) debbyPlay.days.push (allDays[j]);
	}}
	var containerDays = document.getElementsByTagName ('section')[1];
	containerDays.load();
	addSubTitles();
}
function addSubTitles(){
	var title, parag = document.getElementsByTagName ('p');
	for (var p=0; p< parag.length; p++) if (parag[p].innerHTML.contain ('______ ')){
		title = document.createElement ('h3');
		title.innerHTML = parag[p].innerHTML.slice (7,-7);
		parag[p].parentElement.insertBefore (title, parag[p]);
		parag[p].parentElement.removeChild (parag[p]);
}}