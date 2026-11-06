"""Initial Schema Baseline Migration (All 14 Tables)

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-11-06 18:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    # 1. USERS
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('username', sa.String(100), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('system_role', sa.String(20), nullable=False, server_default='STANDARD_USER'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('failed_login_attempts', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('locked_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_username', 'users', ['username'])

    # 2. USER_VERIFICATIONS
    op.create_table(
        'user_verifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token_hash', sa.String(64), nullable=False, unique=True),
        sa.Column('token_type', sa.String(30), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_verifications_token', 'user_verifications', ['token_hash', 'token_type'])

    # 3. USER_SESSIONS
    op.create_table(
        'user_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('session_token_hash', sa.String(64), nullable=False, unique=True),
        sa.Column('ip_address', postgresql.INET(), nullable=False),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_sessions_token', 'user_sessions', ['session_token_hash'])

    # 4. PROJECTS
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_projects_owner', 'projects', ['owner_id'])

    # 5. PROJECT_MEMBERS
    op.create_table(
        'project_members',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(30), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.UniqueConstraint('project_id', 'user_id', name='uq_project_member'),
    )
    op.create_index('idx_project_members_lookup', 'project_members', ['project_id', 'user_id'])

    # 6. SCRIPTS
    op.create_table(
        'scripts',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_scripts_project', 'scripts', ['project_id'])

    # 7. SCRIPT_VERSIONS
    op.create_table(
        'script_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('script_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scripts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('is_current', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('original_filename', sa.String(255), nullable=False),
        sa.Column('file_format', sa.String(20), nullable=False),
        sa.Column('storage_path', sa.String(500), nullable=False),
        sa.Column('file_size', sa.BigInteger(), nullable=False),
        sa.Column('file_hash', sa.String(64), nullable=False),
        sa.Column('is_ocr_applied', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('ocr_confidence', sa.Numeric(5, 2), nullable=True),
        sa.Column('processing_status', sa.String(30), nullable=False, server_default='QUEUED'),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.UniqueConstraint('script_id', 'version_number', name='uq_script_version_num'),
    )
    # Circular FK eliminated via partial unique index
    op.execute(
        'CREATE UNIQUE INDEX idx_single_current_version ON script_versions (script_id) WHERE is_current = TRUE;'
    )

    # 8. PROCESSING_JOBS
    op.create_table(
        'processing_jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('script_version_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('script_versions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('job_type', sa.String(30), nullable=False),
        sa.Column('status', sa.String(30), nullable=False, server_default='QUEUED'),
        sa.Column('progress_percent', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('queue_name', sa.String(50), nullable=False, server_default='default'),
        sa.Column('worker_id', sa.String(100), nullable=True),
        sa.Column('attempt_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('max_retries', sa.Integer(), nullable=False, server_default=sa.text('3')),
        sa.Column('error_code', sa.String(50), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('heartbeat_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_processing_jobs_queue', 'processing_jobs', ['status', 'created_at'])

    # 9. SCENES
    op.create_table(
        'scenes',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('script_version_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('script_versions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('sequence_index', sa.Integer(), nullable=False),
        sa.Column('scene_number', sa.String(20), nullable=True),
        sa.Column('slugline', sa.Text(), nullable=False),
        sa.Column('setting', sa.String(200), nullable=True),
        sa.Column('time_of_day', sa.String(50), nullable=True),
        sa.Column('int_ext', sa.String(20), nullable=True),
        sa.Column('page_start', sa.Integer(), nullable=False),
        sa.Column('page_end', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.UniqueConstraint('script_version_id', 'sequence_index', name='uq_scene_sequence'),
    )
    op.create_index('idx_scenes_version', 'scenes', ['script_version_id'])

    # 10. SCENE_ELEMENTS
    op.create_table(
        'scene_elements',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('scene_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scenes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('sequence_index', sa.Integer(), nullable=False),
        sa.Column('element_type', sa.String(30), nullable=False),
        sa.Column('character_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('raw_text', sa.Text(), nullable=False),
        sa.Column('page_number', sa.Integer(), nullable=False),
        sa.Column('line_start', sa.Integer(), nullable=False),
        sa.Column('line_end', sa.Integer(), nullable=False),
        sa.Column('bounding_box', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.UniqueConstraint('scene_id', 'sequence_index', name='uq_element_sequence'),
    )
    op.create_index('idx_scene_elements_scene', 'scene_elements', ['scene_id'])

    # 11. CHARACTERS
    op.create_table(
        'characters',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('script_version_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('script_versions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('canonical_name', sa.String(100), nullable=False),
        sa.Column('total_speeches', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('first_scene_sequence', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.UniqueConstraint('script_version_id', 'canonical_name', name='uq_character_name'),
    )

    # 12. CHARACTER_ALIASES
    op.create_table(
        'character_aliases',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('character_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('characters.id', ondelete='CASCADE'), nullable=False),
        sa.Column('alias', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )

    # 13. ANALYSIS_RUNS
    op.create_table(
        'analysis_runs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('script_version_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('script_versions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('analysis_type', sa.String(50), nullable=False),
        sa.Column('provider', sa.String(50), nullable=False),
        sa.Column('model', sa.String(100), nullable=False),
        sa.Column('prompt_version', sa.String(20), nullable=False),
        sa.Column('status', sa.String(30), nullable=False, server_default='QUEUED'),
        sa.Column('tokens_prompt', sa.Integer(), nullable=True),
        sa.Column('tokens_completion', sa.Integer(), nullable=True),
        sa.Column('estimated_cost_usd', sa.Numeric(8, 4), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )

    # 14. ANALYSIS_RESULTS
    op.create_table(
        'analysis_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('analysis_run_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('analysis_runs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('scene_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scenes.id', ondelete='CASCADE'), nullable=True),
        sa.Column('character_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('characters.id', ondelete='CASCADE'), nullable=True),
        sa.Column('result_type', sa.String(50), nullable=False),
        sa.Column('result_data', postgresql.JSONB(), nullable=False),
        sa.Column('confidence', sa.Numeric(5, 2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_analysis_results_run', 'analysis_results', ['analysis_run_id'])
    op.execute('CREATE INDEX idx_analysis_results_gin ON analysis_results USING gin (result_data);')

    # 15. AUDIT_LOGS
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('ip_address', postgresql.INET(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )
    op.create_index('idx_audit_logs_user', 'audit_logs', ['user_id'])
    op.create_index('idx_audit_logs_action', 'audit_logs', ['action'])


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('analysis_results')
    op.drop_table('analysis_runs')
    op.drop_table('character_aliases')
    op.drop_table('characters')
    op.drop_table('scene_elements')
    op.drop_table('scenes')
    op.drop_table('processing_jobs')
    op.drop_table('script_versions')
    op.drop_table('scripts')
    op.drop_table('project_members')
    op.drop_table('projects')
    op.drop_table('user_sessions')
    op.drop_table('user_verifications')
    op.drop_table('users')
