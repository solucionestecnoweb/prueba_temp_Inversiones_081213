# -*- coding: utf-8 -*-

{
        'name': 'Product Moves invoice',
        'version': '0.1',
        'author': 'INM & LDR Soluciones Tecnológicas y Empresariales C.A',
        'summary': '',
        'description': """""",
        'category': 'Accounting/Accounting',
        'website': '',
        'images': [],
        'depends': [
            'stock',
            'account',
            'sale',
            'sale_stock',
            'ext_yoko_formato_factura_nd_nc',
            'l10n_ve_fiscal_requirements',
            ],
        'data': [
            'views/stock_move_line_views.xml',
            'views/stock_picking_views.xml'
                 ],
        'installable': True,
        'application': False,
        'auto_install': False,
                      
}
