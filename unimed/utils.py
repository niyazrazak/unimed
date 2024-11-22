
import frappe

@frappe.whitelist()
def get_street_address(party_type, party):
	address_list = frappe.db.sql(
			"""
			SELECT
				link.parent
			FROM
				`tabDynamic Link` link,
				`tabAddress` address
			WHERE
				link.parenttype = "Address"
					AND link.link_name = %(party)s
			ORDER BY
				address.address_type="Postal" DESC,
				address.address_type="Billing" DESC
			LIMIT 1
		""",
			{"party": party},
			as_dict=True
		)
	if address_list:
		party_address = address_list[0]["parent"]
		doc = frappe.get_doc("Address", party_address)


		return doc.as_dict()
	return address_list


@frappe.whitelist()
def get_bank_detaiks(company):
	bank_details = frappe.db.get_value("Bank Account", {
		"company": company,
		"is_company_account": 1,
		"is_default": 1,
		"disabled": 0
	}, ["account_name", "bank_account_no", "iban", "bank", "branch_code"], as_dict=1)
	if bank_details:
		bank_details['swift_number'] = frappe.db.get_value("Bank", bank_details.get("bank"), "swift_number")
	return bank_details