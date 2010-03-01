var Ext;
Ext.ns('Ext.nitrol');

Ext.nitrol.rankRenderer = function (num) {
	return num > 0 ? num.toString() + 'd' : (Math.abs(num) + 1).toString() + 'k';
}

Ext.nitrol.tickCross = function (val) {
	return val ? '&#x2714;' : '&#x2718;'
}

Ext.nitrol.grid = new Ext.grid.GridPanel({
		store: new Ext.data.JsonStore({
				remoteSort: false,
				url: 'players/getindex',
				root: 'data',
				fields: [
					'id',
					'pin',
					'first_name',
					'last_name',
					'club',
					'rank',
					'rank_num',
					'egf',
					'confirmed'
				]
			}),
		columns: [
			{header: 'Imię', dataIndex: 'first_name', sortable: true},
			{header: 'Nazwisko', dataIndex: 'last_name', sortable: true},
			{header: 'Klub', dataIndex: 'club', sortable: true},
			{header: 'Siła', dataIndex: 'rank_num', sortable: true, renderer: Ext.nitrol.rankRenderer},
			{header: 'EGF', dataIndex: 'egf', sortable: true},
			{header: 'Potwierdzone', dataIndex: 'confirmed', sortable: true, renderer: Ext.nitrol.tickCross}
		],
		tbar: [
			{
				text: 'Nowy',
				iconCls: 'icon-add',
				handler: function () {
					if (!Ext.isDefined(Ext.nitrol.addPopup)) {
						Ext.nitrol.addPopup = new Ext.nitrol.AddPopup();
						Ext.nitrol.addPopup.show();
					} 
				}
			}
		],
		region: 'center',
		viewConfig: {autoFill: true}
	});


Ext.onReady(function () {
		Ext.QuickTips.init();
		Ext.nitrol.vp = new Ext.Viewport({
				items: [Ext.nitrol.grid],
				layout: 'border'
			});
		Ext.nitrol.grid.store.load();
	})
