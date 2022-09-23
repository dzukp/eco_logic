function update() {
	var i = 0
	for (var i = 1; i < 11; i++) {
		var val = getTag('main', 'p' + i + '_cmd').getValue()
		if ((val & 0x8000) == 0) {
			break
		}
	}
	getGlobalVar('post_count').setIntData(i - 1)
}
