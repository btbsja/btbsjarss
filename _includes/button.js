function show_all() {
	var but = document.getElementsByClassName('category-but');
	for (var i = but.length - 1; i >= 0; i--) {
		if ('all' == but[i].value) {
			but[i].style.backgroundColor = '#555555';
			but[i].style.color = '#ffffff';
		} else {
			but[i].style.backgroundColor = '#e7e7e7';
			but[i].style.color = '#000000';
		}
	}
	var cat = document.getElementsByClassName('post-card');
	for (var i = cat.length - 1; i >= 0; i--) {
		cat[i].style.display = 'list-item';
	}
}

function show_and_hide(category) {
	var but = document.getElementsByClassName('category-but');
	for (var i = but.length - 1; i >= 0; i--) {
		if (category.value == but[i].value) {
			but[i].style.backgroundColor = '#555555';
			but[i].style.color = '#ffffff';
		} else {
			but[i].style.backgroundColor = '#e7e7e7';
			but[i].style.color = '#000000';
		}
	}
	var cat = document.getElementsByClassName('post-card');
	for (var i = cat.length - 1; i >= 0; i--) {
		if (cat[i].id == category.value) {
			cat[i].style.display = 'list-item';
		} else {
			cat[i].style.display = 'none';
		}
	}
}