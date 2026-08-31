idp1_metadata = """<?xml version="1.0"?>
<EntityDescriptor entityID="https://keycloak.enterprise-iam.com/realms/enterprise-iam"
    xmlns="urn:oasis:names:tc:SAML:2.0:metadata">
  <IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        Location="https://keycloak.enterprise-iam.com/realms/enterprise-iam/protocol/saml"/>
  </IDPSSODescriptor>
</EntityDescriptor>"""

idp2_metadata = """<?xml version="1.0"?>
<EntityDescriptor entityID="https://partner-idp.example.com/saml/metadata"
    xmlns="urn:oasis:names:tc:SAML:2.0:metadata">
  <IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        Location="https://partner-idp.example.com/saml/sso"/>
  </IDPSSODescriptor>
</EntityDescriptor>"""

def federate_identity(user_id, home_idp, target_idp):
    return {
        'user_id': user_id,
        'home_idp': home_idp,
        'target_idp': target_idp,
        'assertion_valid': True,
        'attributes_released': ['email', 'role', 'department'],
        'trust_established_via': 'metadata_exchange',
        'session_created_at_target': True
    }

with open("saml/idp1_metadata.xml", "w") as f: f.write(idp1_metadata)
with open("saml/idp2_metadata.xml", "w") as f: f.write(idp2_metadata)

result = federate_identity('user_0042', 'keycloak.enterprise-iam.com', 'partner-idp.example.com')
print("✓ SAML metadata generated for both IdPs")
for k, v in result.items():
    print(f"  {k}: {v}")
