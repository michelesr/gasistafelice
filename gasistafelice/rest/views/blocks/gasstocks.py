from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction
from gasistafelice.consts import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response

from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.forms.stocks import GASSupplierStockFormSet

from flexi_auth.models import ObjectWithContext

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "gasstocks"
    BLOCK_DESCRIPTION = _("GAS Stocks")
    BLOCK_VALID_RESOURCE_TYPES = ["pact"] 

    COLUMN_INDEX_NAME_MAP = {
        0: 'pk',
        1: 'stock__product',
        2: 'stock__product__description',
        3: 'price',
        4: 'stock__availability',
        5: 'enabled'
    }

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):
            user_actions += [
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=VIEW, verbose_name=_("Show"), 
                    popup_form=False,
                    method="get",
                ),
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=EDIT_MULTIPLE, verbose_name=_("Edit"), 
                    popup_form=False,
                    method="get",
                ),
            ]

        return user_actions

    def _get_resource_list(self, request):
        #GASSupplierStock
        return request.resource.gasstocks

    def _get_edit_multiple_form_class(self):
        return GASSupplierStockFormSet

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        data = {}
        i = 0
        
        for i,el in enumerate(querySet):
            key_prefix = 'form-%d' % i
            data.update({
               '%s-id' % key_prefix : el.pk,
               '%s-pk' % key_prefix : el.pk,
               '%s-enabled' % key_prefix : el.enabled,
            })

        data['form-TOTAL_FORMS'] = i + 1
        data['form-INITIAL_FORMS'] = i + 1
        data['form-MAX_NUM_FORMS'] = 0

        formset = GASSupplierStockFormSet(request, data)

        records = []
        for i,form in enumerate(formset):

            records.append({
               'id' : "%s %s " % (form['pk'], form['id']),
               'product' : querySet[i].stock.product,
               'description' : querySet[i].stock.product.description,
               'price' : querySet[i].price,
               'availability' : querySet[i].stock.amount_available, 
               'field_enabled' : [_('not available'),form['enabled']][bool(querySet[i].enabled)],
            })

        return formset, records, {}

