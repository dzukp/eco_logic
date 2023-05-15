function selectPost(number) {
	var prefix = 'p' + number + '_'	

	getGlobalVar('selected_post').setIntData(number)

	getGlobalVar('post_cmd').setBindSpeaker(getTag('main', prefix + 'cmd'))
	getGlobalVar('post_status').setBindSpeaker(getTag('main', prefix + 'status'))
	getGlobalVar('post_pressure').setBindSpeaker(getTag('main', prefix + 'pressure'))
	getGlobalVar('post_func_number').setBindSpeaker(getTag('main', prefix + 'number'))

	var mechs = ['foam', 'wax', 'shampoo', 'cold_water', 'hot_water', 'osmos', 'out_water', 'out_foam', 'intensive', 'hoover']
	for (var i = 0; i < mechs.length; i++ ) {
		var s = mechs[i]

		getGlobalVar('post_v_' + s + '_cmd').setBindSpeaker(getTag('main', prefix + 'v_' + s + '_cmd'))
		getGlobalVar('post_v_' + s + '_status').setBindSpeaker(getTag('main', prefix + 'v_' + s + '_status'))
	}

	getGlobalVar('post_pump_cmd').setBindSpeaker(getTag('main', prefix + 'pump_cmd'))
	getGlobalVar('post_pump_status').setBindSpeaker(getTag('main', prefix + 'pump_status'))
	getGlobalVar('post_pump_auto_freq').setBindSpeaker(getTag('main', prefix + 'pump_auto_freq'))
	getGlobalVar('post_pump_man_freq').setBindSpeaker(getTag('main', prefix + 'pump_man_freq'))
	getGlobalVar('post_pump_out_freq').setBindSpeaker(getTag('main', prefix + 'pump_out_freq'))
	getGlobalVar('post_pump_alarm').setBindSpeaker(getTag('main', prefix + 'pump_alarm'))
}
