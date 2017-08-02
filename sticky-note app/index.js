window.onload = function(){
	var dashboard = document.getElementById('dashboard');
	var id = -1;
	document.getElementById("add").onclick=function(){
		id++;
		//console.log(document.getElementById('dashboard'))
		var new_note = dashboard.appendChild(document.createElement('div'));	
		new_note.className = "note"
		new_note.id = "new_note-"+id

		var close = new_note.appendChild(document.createElement('span'))
		close.className = "close"
		close.innerHTML = 'X'
		close.onclick=function(){
			dashboard.removeChild(new_note)
		}
		var edit = new_note.appendChild(document.createElement('edit'))
		edit.className = "edit"
		edit.innerHTML = "D"

		var textbox = new_note.appendChild(document.createElement('input'))
		textbox.className = "textbox"
		textbox.size = "15"
		textbox.maxLength = "15"
		textbox.id = "textbox-"+id;

		var textarea = new_note.appendChild(document.createElement('textarea'))
		textarea.className = "textarea"
		textarea.maxLength = "300"
		textarea.id = "textarea-"+id;

		edit.onclick=function()
		{
			var textboxnow = document.createElement((edit.innerHTML == "D")? 'div': 'input')
			textbox = document.getElementById("textbox-"+id)
			textboxnow.className = "textbox"

			var textareanow = document.createElement((edit.innerHTML == "D")? 'div' :'textarea')
			textarea = document.getElementById("textarea-"+id)
			textareanow.className = "textarea"

			if (edit.innerHTML == "D")
			{
				edit.innerHTML = "E";
				textboxnow.innerHTML = textbox.value
				textareanow.innerHTML = textarea.value
			}
			else
			{
				edit.innerHTML = "D";
				textboxnow.value = textbox.innerHTML
				textboxnow.size = "15"
				textboxnow.maxLength = "15"

				textareanow.value = textarea.innerHTML
				textareanow.maxLength = "300"				
			}

			new_note.replaceChild(textboxnow, textbox)
			textboxnow.id = "textbox-"+id

			new_note.replaceChild(textareanow, textarea)
			textareanow.id = "textarea-"+id
		}

		var colors = ["rgb(255, 0, 0)", "rgb(0, 255, 0)", "rgb(0, 0, 255)", "rgb(255, 255, 255)","rgb(0, 0, 0)"];
		for (var i=0; i<colors.length; i++)
		{
			var color = new_note.appendChild(document.createElement('div'))
			color.style.height = "30px";
			color.style.width = "30px";
			color.style.marginLeft = "10px";
			color.style.marginTop = "7px";
			color.style.float = "left";
			color.style.backgroundColor = colors[i];
			color.id = i;
			color.onclick=function(){
				new_note.style.backgroundColor = colors[this.id];
			}
		}
		

	}
}