import json

KEYCLOAK_REALM = {
    "realm": "enterprise-iam",
    "displayName": "Enterprise IAM Platform",
    "enabled": True,
    "bruteForceProtected": True,
    "failureFactor": 5,
    "passwordPolicy": "length(12) and upperCase(1) and specialChars(1)",
    "accessTokenLifespan": 300,
    "roles": {
        "realm": [
            {"name": "standard_user",
             "description": "Regular employee"},
            {"name": "privileged_user",
             "description": "IT Administrator"},
            {"name": "auditor",
             "description": "Compliance read-only"}
        ]
    },
    "users": [
        {
            "username": "john.doe",
            "email": "john.doe@enterprise.com",
            "enabled": True,
            "realmRoles": ["standard_user"],
            "credentials": [{
                "type": "password",
                "value": "SecurePass@123"
            }]
        },
        {
            "username": "admin.smith",
            "email": "admin.smith@enterprise.com",
            "enabled": True,
            "realmRoles": ["privileged_user"],
            "credentials": [{
                "type": "password",
                "value": "AdminPass@456"
            }]
        }
    ]
}

with open("keycloak/enterprise-iam-realm.json", "w") as f:
    json.dump(KEYCLOAK_REALM, f, indent=2)

print("✅ Keycloak Realm: enterprise-iam created")
print(f"✅ Roles defined: {[r['name'] for r in KEYCLOAK_REALM['roles']['realm']]}")
print(f"✅ Users configured: {[u['username'] for u in KEYCLOAK_REALM['users']]}")
print("✅ Token lifespan: 300 seconds")
print("✅ Brute force protection: ENABLED")
print("✅ enterprise-iam-realm.json saved")
