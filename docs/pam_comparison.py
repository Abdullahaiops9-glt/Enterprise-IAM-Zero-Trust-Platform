import pandas as pd

pam_comparison = pd.DataFrame({
    'Feature': ['Cost', 'Deployment Model', 'Open Source', 'API-First Design',
                'Kubernetes/Docker Native', 'Secret Rotation', 'Learning Curve',
                'Vendor Lock-in', 'Project Fit'],
    'HashiCorp Vault (Chosen)': ['Free / Open Source', 'Self-hosted, cloud, or hybrid',
                                   'Yes — full source available', 'Yes — built for automation',
                                   'Native, first-class support', 'Automatic, built-in',
                                   'Moderate', 'None', 'Perfect — matches Docker/K8s stack'],
    'CyberArk': ['$$$$ Enterprise licensing', 'Mostly on-prem, enterprise-heavy',
                 'No — proprietary', 'Limited, GUI-first',
                 'Limited, requires connectors', 'Yes, but licensed feature',
                 'Steep — enterprise training needed', 'High', 'Cost barrier for EduQual project']
})

print("✓ PAM Tool Comparison Generated\n")
print(pam_comparison.to_string(index=False))

print("\n--- Why HashiCorp Vault Was Chosen ---")
reasons = [
    "Zero licensing cost — appropriate for an EduQual diploma project",
    "Native Docker/Kubernetes integration matches this project's deployment model",
    "API-first design allows direct integration with the Risk Engine and PDP",
    "Open source — every configuration decision is inspectable and defensible",
    "CyberArk's strengths (enterprise workflow, GUI policy management) matter more",
    "  at large-enterprise scale than at this project's scope"
]
for r in reasons:
    print(f"  • {r}")
