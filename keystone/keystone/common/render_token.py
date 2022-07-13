from keystone.common import provider_api
import keystone.conf


CONF = keystone.conf.CONF
PROVIDERS = provider_api.ProviderAPIS


def render_token_response_from_model(token, include_catalog=True):
    token_reference = {
        'token': {
            'methods': token.methods,
            'user': {
                'domain': {
                    'id': token.user_domain['id'],
                    'name': token.user_domain['name']
                },
                'id': token.user_id,
                'name': token.user['name'],
                'password_expires_at': token.user[
                    'password_expires_at'
                ]
            },
            'audit_ids': token.audit_ids,
            'expires_at': token.expires_at,
            'issued_at': token.issued_at,
        }
    }
    if token.system_scoped:
        token_reference['token']['roles'] = token.roles
        token_reference['token']['system'] = {'all': True}
    elif token.domain_scoped:
        token_reference['token']['domain'] = {
            'id': token.domain['id'],
            'name': token.domain['name']
        }
        token_reference['token']['roles'] = token.roles
    elif token.trust_scoped:
        token_reference['token']['OS-TRUST:trust'] = {
            'id': token.trust_id,
            'trustor_user': {'id': token.trustor['id']},
            'trustee_user': {'id': token.trustee['id']},
            'impersonation': token.trust['impersonation']
        }
        token_reference['token']['project'] = {
            'domain': {
                'id': token.project_domain['id'],
                'name': token.project_domain['name']
            },
            'id': token.trust_project['id'],
            'name': token.trust_project['name']
        }
        if token.trust.get('impresonation'):
            trustor_domain = PROVIDERS.resource_api.get_domain(
                token.trustor['domain_id']
            )
            token_reference['token']