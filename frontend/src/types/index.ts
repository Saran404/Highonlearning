/** Shared TypeScript interfaces that mirror the FastAPI schemas. */

export type Role = 'STUDENT' | 'ADMIN' | 'INSTRUCTOR';
export type LockStatus = 'LOCKED' | 'AVAILABLE' | 'IN_PROGRESS' | 'COMPLETED';
export type AttemptStatus = 'IN_PROGRESS' | 'SUBMITTED' | 'AUTO_SUBMITTED' | 'FLAGGED';
export type AttemptType = 'GRADED' | 'PRACTICE';
export type MalpracticeType = 'TAB_SWITCH' | 'MINIMIZE' | 'FULLSCREEN_EXIT' | 'DEVTOOLS' | 'COPY_PASTE' | 'RIGHT_CLICK';
export type TriggerType = 'START' | 'INTERVAL' | 'MALPRACTICE' | 'END';

export interface User {
  id: number;
  name: string;
  email: string;
  role: Role;
  avatar_url?: string | null;
  created_at: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: User;
  device_id: string;
  session_id: string;
}

export interface ApiErrorBody {
  code: string;
  message: string;
  details?: unknown;
}

export interface Course {
  id: number;
  title: string;
  slug: string;
  description?: string | null;
  thumbnail_url?: string | null;
  order_index: number;
  graded_count: number;
  practice_count: number;
  completed_count: number;
  enrolled: boolean;
  lock_status?: LockStatus;
  previous_course_title?: string | null;
  previous_course_slug?: string | null;
}

export interface AssessmentItem {
  id: number;
  course_id: number;
  title: string;
  title_ta?: string | null;
  slug: string;
  description?: string | null;
  description_ta?: string | null;
  topic?: string | null;
  difficulty?: 'EASY' | 'MEDIUM' | 'HARD' | null;
  default_duration_minutes: number;
  min_duration_minutes: number;
  total_questions: number;
  pass_percentage: number;
  attempt_type: AttemptType;
  sequential_unlock: boolean;
  lockdown_enabled: boolean;
  proctoring_enabled: boolean;
  order_index: number;
  lock_status: LockStatus;
  attempt_id?: number | null;
  score?: number | null;
  total?: number | null;
  percentage?: number | null;
  time_taken_sec?: number | null;
  rank_position?: number | null;
  total_participants?: number | null;
  course_slug?: string | null;
  course_title?: string | null;
}

export interface Question {
  id: number;
  text: string;
  options: string[];
  text_ta?: string | null;
  options_ta?: string[] | null;
  topic?: string | null;
  difficulty?: string | null;
}

export interface SavedAnswer {
  question_id: number;
  selected_index: number | null;
  marked_for_review: boolean;
}

export interface AttemptState {
  attempt_id: number;
  assessment_id: number;
  assessment_title: string;
  status: AttemptStatus;
  questions: Question[];
  saved_answers: SavedAnswer[];
  started_at: string;
  deadline_at: string;
  server_time: string;
  default_duration_minutes: number;
  chosen_duration_minutes: number;
  extended: boolean;
  malpractice_count: number;
  max_malpractice: number;
  lockdown_enabled: boolean;
  proctoring_enabled: boolean;
}

export interface ResultQuestion {
  question_id: number;
  question_text: string;
  options: string[];
  question_text_ta?: string | null;
  options_ta?: string[] | null;
  correct_index: number;
  selected_index: number | null;
  explanation?: string | null;
  explanation_ta?: string | null;
  is_correct: boolean;
  topic?: string | null;
}

export interface Snapshot {
  snapshot_id: number;
  image_url: string;
  captured_at: string;
  trigger_type: TriggerType;
  face_detected?: boolean | null;
  face_match_score?: number | null;
}

export interface ResultResponse {
  attempt: {
    attempt_id: number;
    assessment_id: number;
    assessment_title: string;
    course_id?: number | null;
    course_slug?: string | null;
    course_title?: string | null;
    status: AttemptStatus;
    score: number;
    total: number;
    percentage: number;
    passed: boolean;
    pass_percentage: number;
    time_taken_sec: number;
    rank_position: number | null;
    total_participants: number;
    malpractice_count: number;
    chosen_duration_minutes: number;
    submitted_at?: string | null;
  };
  motivational_message: string;
  questions: ResultQuestion[];
  snapshots: Snapshot[];
}

export interface DashboardStats {
  courses_enrolled: number;
  courses_completed?: number;
  courses_total?: number;
  assessments_completed: number;
  assessments_total: number;
  avg_percentage: number;
  best_rank: number | null;
  completion_percentage: number;
}

export interface DashboardData {
  stats: DashboardStats;
  assessments: AssessmentItem[];
  continue_item: AssessmentItem | null;
}

export interface LeaderboardEntry {
  rank: number;
  name: string;
  score: number;
  total: number;
  percentage: number;
  time_taken_sec: number;
  is_me: boolean;
}

export interface LeaderboardResponse {
  assessment_id: number;
  total_participants: number;
  entries: LeaderboardEntry[];
  me: LeaderboardEntry | null;
}

/* ---------------------------------------------------------------- admin */
export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface StudentRow {
  id: number;
  name: string;
  email: string;
  is_active: boolean;
  has_active_session: boolean;
  last_seen_at?: string | null;
  attempts_count: number;
  created_at: string;
}

export interface AttemptRow {
  attempt_id: number;
  user_id: number;
  user_name: string;
  user_email: string;
  assessment_id: number;
  assessment_title: string;
  status: AttemptStatus;
  started_at: string;
  deadline_at: string;
  submitted_at?: string | null;
  score?: number | null;
  total?: number | null;
  percentage?: number | null;
  time_taken_sec?: number | null;
  rank_position?: number | null;
  malpractice_count: number;
}

export interface AlertRow {
  log_id: number;
  attempt_id: number;
  user_email: string;
  user_name: string;
  assessment_title: string;
  type: MalpracticeType;
  occurred_at: string;
  malpractice_count: number;
  attempt_status: AttemptStatus;
}

export interface LiveAttemptRow {
  attempt_id: number;
  user_name: string;
  user_email: string;
  assessment_title: string;
  started_at: string;
  deadline_at: string;
  malpractice_count: number;
}

export interface AttemptDrilldownData {
  attempt: AttemptRow;
  answers: {
    question_id: number;
    question_text: string;
    selected_index: number | null;
    correct_index: number;
    is_correct: boolean;
    marked_for_review: boolean;
  }[];
  malpractice_logs: { log_id: number; type: MalpracticeType; occurred_at: string; metadata?: unknown }[];
  snapshots: Snapshot[];
}

export type AdminEvent =
  | { type: 'STUDENT_STARTED'; attempt_id: number; user_email: string; assessment: string }
  | { type: 'MALPRACTICE_ALERT'; attempt_id: number; user_email: string; count: number; latest_type: MalpracticeType; terminated?: boolean }
  | { type: 'ATTEMPT_SUBMITTED'; attempt_id: number; user_email: string; score: number; percentage: number; status?: AttemptStatus };

export interface FeedItem {
  id: string;
  at: number;
  event: AdminEvent;
}

export interface ReflectionAnswerItem {
  question_number: number;
  question: string;
  selected_option: string;
}

export interface ReflectionResponse {
  course_id: number;
  course_slug: string;
  course_title: string;
  submitted: boolean;
  submitted_at?: string | null;
  answers: ReflectionAnswerItem[];
}

export interface UserCourseReflection {
  course_id: number;
  course_slug: string;
  course_title: string;
  submitted_at: string;
  updated_at: string;
  answers: ReflectionAnswerItem[];
}

export interface AdminUserReflectionSummary {
  user_id: number;
  name: string;
  email: string;
  total_reflections: number;
  latest_submitted_at?: string | null;
  courses: UserCourseReflection[];
}

