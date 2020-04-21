/*
Javascript enabling to filter words with the ones already present in the database.
Requirements :
* The javascript variable target words should be defined and defines the id of the input box for words
The HTML script should follow the current convention :
<div class="adding_word">
	<fieldset>
		<legend>Original word</legend>
		<div class="row">
		  <div class="col-6">
			{{ form.word|as_crispy_field }}
		  </div>
		  <div class="col-2">
			{{ form.gender|as_crispy_field }}
		  </div>
		  <div class="col-4">
			{{ form.language|as_crispy_field }}
		  </div>
		</div>
		<ul class="list-group list_words" style="display:none">
		  {% for key, values in words.items %}
			<li class="list-group-item" onClick="choose(this,'id_{{ form.prefix }}','{{ values.0 }}',{{ values.1}} , {{ values.2 }});">{{ values.0 }}</li>
		  {% endfor %}
		</ul>
	</fieldset>
</div>
*/

function get_variable_like_string(item){
	// Number should be simply displayed, but string should be between quotes
	//console.log("New item : "+item);
	if(item==""){
		//console.log("empty");
		return "''";
	}
	else if(typeof item === 'number') {	
		//console.log("number : "+item);
		return item;
	}
	else if(typeof item === "string"){
		//console.log("string : "+item);
		return "'"+item+"'";
	}
	else{
		//console.log("Don't know how to handle : "+item);
		return item;
	}
}

function get_array_like_string(arr){
	
	str = "[";
	var i;
	for (i = 0; i < arr.length; i++) {
	  str += get_variable_like_string(arr[i]);
	  if(i!=arr.length-1){
		  str += ",";
	  }
	} 
	str += "]";
	return str
	
}

$(document).ready(function(){
  $(target_words).on("keyup", function() {
	
	console.log("Been here");
	
	var input, filter, list_words, li, a, i, txtValue, form_adding_word;
	
	form_adding_word = this.closest(".adding_item") // Getting the div surrounding the subform to "Add a word"
	list_words = form_adding_word.getElementsByTagName("ul")[0];
	list_words.style.display = "block";
	
	var parameters = form_adding_word.getElementsByClassName("parameters")[0];
	var prefix = parameters.getElementsByClassName("prefix")[0].innerText;
	var list_fields = parameters.getElementsByClassName("list_fields")[0].innerText;
	var url_autocomplete = parameters.getElementsByClassName("url_autocomplete")[0].innerText;

	filter = this.value;
	$.ajax({
		url: url_autocomplete,
		data: {
		  'search': filter 
		},
		dataType: 'json',
		success: function (data) {
			list = data.list;
			list_words.innerHTML = ""
			$.each(list, function(i)
			{
				var x = get_array_like_string(list[i]);
				var li = $('<li/>')
				.addClass('list-group-item')
				.css({'cursor': "pointer"})
				.attr('onClick', "choose(this,'id_"+prefix+"',"+list_fields+","+x+");")
				.text(list[i][list[i].length - 1])
				.appendTo(list_words);
			});       
		}
	});    
  });
  
});

function choose(elt,prefix_id,fields,values){
	
	var nb_fields = fields.length;

	form_adding_word = elt.closest(".adding_item") // Getting the div surrounding the subform to "Add a word"
	list_words = form_adding_word.getElementsByTagName("ul")[0];

	for (var i = 0; i < nb_fields; i++) {
		document.getElementById(String(prefix_id)+"-"+String(fields[i])).value = String(values[i]);
	}
	
	// TODO : using elt to locate myself and apply new style
	list_words.style.display = "None";
	
	return;

}