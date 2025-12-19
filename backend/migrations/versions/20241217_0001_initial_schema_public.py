"""Initial schema public - Tabelas globais da Legia

Revision ID: 0001
Revises:
Create Date: 2024-12-17 00:01:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Cria todas as tabelas do schema public (dados globais da Legia)
    """

    # ========== PLANS ==========
    op.create_table(
        'plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price_monthly', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('price_yearly', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('max_users', sa.Integer(), nullable=True),
        sa.Column('max_clients', sa.Integer(), nullable=True),
        sa.Column('max_storage_gb', sa.Integer(), nullable=True),
        sa.Column('max_processes_month', sa.Integer(), nullable=True),
        sa.Column('features', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('color', sa.String(length=7), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('display_order', sa.Integer(), server_default='0'),
        sa.Column('is_public', sa.Boolean(), server_default='true'),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )
    op.create_index('ix_plans_slug', 'plans', ['slug'], unique=True, schema='public')

    # ========== TENANTS ==========
    op.create_table(
        'tenants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('subdomain', sa.String(length=100), nullable=False),
        sa.Column('cnpj', sa.String(length=18), nullable=False),
        sa.Column('crc', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='trial'),
        sa.Column('plan_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('trial_ends_at', sa.DateTime(), nullable=True),
        sa.Column('activated_at', sa.DateTime(), nullable=True),
        sa.Column('suspended_at', sa.DateTime(), nullable=True),
        sa.Column('canceled_at', sa.DateTime(), nullable=True),
        sa.Column('logo_url', sa.String(length=500), nullable=True),
        sa.Column('primary_color', sa.String(length=7), server_default='#004E89'),
        sa.Column('secondary_color', sa.String(length=7), server_default='#FF6B35'),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('address_street', sa.String(length=255), nullable=True),
        sa.Column('address_number', sa.String(length=20), nullable=True),
        sa.Column('address_complement', sa.String(length=100), nullable=True),
        sa.Column('address_neighborhood', sa.String(length=100), nullable=True),
        sa.Column('address_city', sa.String(length=100), nullable=True),
        sa.Column('address_state', sa.String(length=2), nullable=True),
        sa.Column('address_zipcode', sa.String(length=10), nullable=True),
        sa.Column('custom_domain', sa.String(length=255), nullable=True),
        sa.Column('custom_domain_verified', sa.Boolean(), server_default='false'),
        sa.Column('settings', postgresql.JSON(astext_type=sa.Text()), server_default='{}'),
        sa.Column('extra_data', postgresql.JSON(astext_type=sa.Text()), server_default='{}'),
        sa.ForeignKeyConstraint(['plan_id'], ['public.plans.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )
    op.create_index('ix_tenants_subdomain', 'tenants', ['subdomain'], unique=True, schema='public')
    op.create_index('ix_tenants_cnpj', 'tenants', ['cnpj'], unique=True, schema='public')
    op.create_index('ix_tenants_status', 'tenants', ['status'], schema='public')

    # ========== SUBSCRIPTIONS ==========
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='active'),
        sa.Column('billing_cycle', sa.String(length=20), nullable=False, server_default='monthly'),
        sa.Column('current_period_start', sa.Date(), nullable=False),
        sa.Column('current_period_end', sa.Date(), nullable=False),
        sa.Column('cancel_at_period_end', sa.Boolean(), server_default='false'),
        sa.Column('canceled_at', sa.DateTime(), nullable=True),
        sa.Column('cancellation_reason', sa.Text(), nullable=True),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), server_default='BRL'),
        sa.Column('extra_users', sa.Integer(), server_default='0'),
        sa.Column('extra_users_price', sa.Numeric(precision=10, scale=2), server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['tenant_id'], ['public.tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['plan_id'], ['public.plans.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )
    op.create_index('ix_subscriptions_tenant', 'subscriptions', ['tenant_id'], schema='public')
    op.create_index('ix_subscriptions_status', 'subscriptions', ['status'], schema='public')

    # ========== PAYMENTS ==========
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('subscription_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), server_default='BRL'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('payment_method', sa.String(length=50), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('gateway_id', sa.String(length=255), nullable=True),
        sa.Column('gateway_status', sa.String(length=100), nullable=True),
        sa.Column('invoice_url', sa.String(length=500), nullable=True),
        sa.Column('boleto_url', sa.String(length=500), nullable=True),
        sa.Column('pix_qrcode', sa.Text(), nullable=True),
        sa.Column('card_last4', sa.String(length=4), nullable=True),
        sa.Column('card_brand', sa.String(length=20), nullable=True),
        sa.Column('failure_code', sa.String(length=50), nullable=True),
        sa.Column('failure_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), server_default='0'),
        sa.Column('extra_data', postgresql.JSON(astext_type=sa.Text()), server_default='{}'),
        sa.ForeignKeyConstraint(['tenant_id'], ['public.tenants.id'], ),
        sa.ForeignKeyConstraint(['subscription_id'], ['public.subscriptions.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )
    op.create_index('ix_payments_tenant', 'payments', ['tenant_id'], schema='public')
    op.create_index('ix_payments_status', 'payments', ['status'], schema='public')
    op.create_index('ix_payments_gateway_id', 'payments', ['gateway_id'], schema='public')

    # ========== LEGIA_USERS ==========
    op.create_table(
        'legia_users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='support'),
        sa.Column('two_factor_enabled', sa.Boolean(), server_default='false'),
        sa.Column('two_factor_secret', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('is_verified', sa.Boolean(), server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.Column('permissions', postgresql.JSON(astext_type=sa.Text()), server_default='{}'),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )
    op.create_index('ix_legia_users_email', 'legia_users', ['email'], unique=True, schema='public')

    print("✅ Schema public criado com sucesso!")


def downgrade() -> None:
    """
    Remove todas as tabelas do schema public
    """
    op.drop_table('payments', schema='public')
    op.drop_table('subscriptions', schema='public')
    op.drop_table('tenants', schema='public')
    op.drop_table('plans', schema='public')
    op.drop_table('legia_users', schema='public')

    print("❌ Schema public removido!")
