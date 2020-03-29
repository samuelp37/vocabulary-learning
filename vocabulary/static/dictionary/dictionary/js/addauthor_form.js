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


$(document).ready(function(){
  $(target_words).on("keyup", function() {
  
	var input, filter, list_words, li, a, i, txtValue, form_adding_word;
	
	form_adding_word = this.closest(".adding_word") // Getting the div surrounding the subform to "Add a word"
	list_words = form_adding_word.getElementsByTagName("ul")[0];
	
	filter = this.value.toUpperCase();
	list_words.style.display = "block";
	li = list_words.getElementsByTagName('li');
	var counter =0;
  
    for (i = 0; i < li.length; i++) {
      a = li[i];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toUpperCase().indexOf(filter) == 0 && counter<3) {
        li[i].style.display = "";
		counter++;
      } else {
        li[i].style.display = "none";
      }
    }
  
  });
  
});

function choose(elt,prefix_id,firstname,lastname){

	form_adding_word = elt.closest(".adding_word") // Getting the div surrounding the subform to "Add a word"
	list_words = form_adding_word.getElementsByTagName("ul")[0];

	document.getElementById(String(prefix_id)+"-first_name").value = String(firstname);
	document.getElementById(String(prefix_id)+"-last_name").value = String(lastname);
	
	// TODO : using elt to locate myself and apply new style
	list_words.style.display = "None";
	
	return;

}