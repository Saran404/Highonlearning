import { ChevronLeft, BookOpen, Dumbbell, Award, Layers, Lock, ArrowRight, Sparkles } from 'lucide-react';
import { useEffect, useState, useRef } from 'react';
import { Link, useParams, useSearchParams, useLocation } from 'react-router-dom';
import { coursesApi } from '../api/courses';
import { toApiError } from '../api/client';
import AssessmentCard from '../components/assessment/AssessmentCard';
import CourseLearnSection from '../components/course/CourseLearnSection';
import CourseReflectiveActivity from '../components/course/CourseReflectiveActivity';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import EmptyState from '../components/common/EmptyState';
import { PageSkeleton } from '../components/common/Skeleton';
import { useAuthStore } from '../store/authStore';
import type { AssessmentItem, Course } from '../types';
import { recordCourseVisited } from '../utils/sessionTracker';

type ActiveTab = 'all' | 'learn' | 'practice' | 'assessments' | 'reflection';
type Language = 'en' | 'ta';

export default function CourseDetailPage() {
  const { slug = '' } = useParams();
  const [searchParams] = useSearchParams();
  const location = useLocation();
  const [course, setCourse] = useState<Course | null>(null);
  const [items, setItems] = useState<AssessmentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<ActiveTab>('all');
  const [language, setLanguage] = useState<Language>(() => {
    const saved = localStorage.getItem('exampro_lang');
    return saved === 'ta' ? 'ta' : 'en';
  });

  const handleLanguageChange = (lang: Language) => {
    setLanguage(lang);
    localStorage.setItem('exampro_lang', lang);
  };

  const learnRef = useRef<HTMLDivElement>(null);
  const practiceRef = useRef<HTMLDivElement>(null);
  const assessmentsRef = useRef<HTMLDivElement>(null);
  const reflectionRef = useRef<HTMLDivElement>(null);

  // Handle ?tab=reflection or #reflection url params
  useEffect(() => {
    const tabParam = searchParams.get('tab') as ActiveTab | null;
    if (tabParam && ['all', 'learn', 'practice', 'assessments', 'reflection'].includes(tabParam)) {
      setActiveTab(tabParam);
      if (tabParam === 'reflection') {
        const timer = setTimeout(() => {
          reflectionRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
        return () => clearTimeout(timer);
      }
    } else if (location.hash === '#reflection') {
      setActiveTab('reflection');
      const timer = setTimeout(() => {
        reflectionRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [searchParams, location.hash, loading]);

  useEffect(() => {
    setLoading(true);
    setError(null);
    coursesApi
      .get(slug)
      .then((c) => {
        setCourse(c);
        const userId = useAuthStore.getState().user?.id;
        if (userId && c) {
          recordCourseVisited(userId, c.slug, c.title);
        }
        if (c.lock_status === 'LOCKED') {
          setItems([]);
          return;
        }
        return coursesApi.assessments(slug).then(setItems);
      })
      .catch((e) => setError(toApiError(e).message))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) return <PageSkeleton />;

  // Locked Course Guard: Show explicit sequential lock state and prerequisite link
  if (course && course.lock_status === 'LOCKED') {
    return (
      <div className="mx-auto max-w-xl py-6">
        <Link to="/courses" className="inline-flex items-center gap-1 text-sm text-sky-700 hover:underline mb-4">
          <ChevronLeft className="h-4 w-4" />Back to Courses
        </Link>
        <Card className="text-center p-6 sm:p-8">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-navy-100 text-navy-500 mb-4">
            <Lock className="h-8 w-8 text-navy-600" />
          </div>
          <span className="inline-flex items-center gap-1.5 rounded-full bg-navy-100 px-3 py-1 text-xs font-bold text-navy-700 uppercase tracking-wider mb-2">
            Sequential Unlock Required
          </span>
          <h1 className="text-2xl font-bold text-navy">{course.title} is Locked</h1>
          <p className="mt-2 text-sm text-navy-600">
            To ensure mastery of prerequisite concepts, courses must be completed in order. You must fully complete the previous course before accessing this one.
          </p>

          {course.previous_course_title && (
            <div className="mt-6 rounded-xl border border-line bg-navy-50/70 p-4 text-left">
              <span className="text-xs font-bold text-navy-500 uppercase tracking-wider">Required Prerequisite:</span>
              <div className="mt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <span className="font-bold text-navy text-base">{course.previous_course_title}</span>
                {course.previous_course_slug && (
                  <Link to={`/courses/${course.previous_course_slug}`}>
                    <Button size="sm" variant="primary" icon={<ArrowRight className="h-4 w-4" />}>
                      Go to Prerequisite
                    </Button>
                  </Link>
                )}
              </div>
            </div>
          )}

          <div className="mt-6 flex flex-col sm:flex-row items-center justify-center gap-3">
            <Link to="/courses" className="w-full sm:w-auto">
              <Button variant="secondary" fullWidth icon={<ChevronLeft className="h-4 w-4" />}>
                View All Courses
              </Button>
            </Link>
          </div>
        </Card>
      </div>
    );
  }

  if (error || !course) {
    const isLockedError = error?.toLowerCase().includes('complete') || error?.toLowerCase().includes('locked');
    return (
      <div className="mx-auto max-w-xl py-6">
        <Card className="text-center p-6 sm:p-8">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-navy-100 text-navy-500 mb-4">
            {isLockedError ? <Lock className="h-8 w-8 text-navy-600" /> : <ChevronLeft className="h-8 w-8 text-navy-600" />}
          </div>
          <h1 className="text-2xl font-bold text-navy">{isLockedError ? 'Course Locked' : 'Course Not Found'}</h1>
          <p className="mt-2 text-sm text-navy-600">{error ?? 'The requested course could not be loaded.'}</p>
          <div className="mt-6 flex justify-center">
            <Link to="/courses">
              <Button variant="secondary" icon={<ChevronLeft className="h-4 w-4" />}>
                Back to Courses
              </Button>
            </Link>
          </div>
        </Card>
      </div>
    );
  }

  // Unified assessment list: eliminate split -en / -ta assessments if unified assessment exists
  const unifiedItems = items.filter((item) => {
    const isSplitLang = item.slug.endsWith('-en') || item.slug.endsWith('-ta');
    if (isSplitLang) {
      const baseSlug = item.slug.replace(/-(en|ta)$/, '');
      if (items.some((o) => o.slug === baseSlug)) return false;
    }
    // Fallback if legacy seed is still in DB: filter by chosen language
    if (item.slug.endsWith('-ta')) return language === 'ta';
    if (item.slug.endsWith('-en')) return language === 'en';
    return true;
  });

  const graded = unifiedItems.filter((i) => i.attempt_type === 'GRADED');
  const practice = unifiedItems.filter((i) => i.attempt_type === 'PRACTICE');
  const allGradedCompleted = graded.length === 0 || graded.every((g) => g.lock_status === 'COMPLETED');

  const scrollToSection = (tab: ActiveTab) => {
    setActiveTab(tab);
    if (tab === 'learn' && learnRef.current) {
      learnRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else if (tab === 'practice' && practiceRef.current) {
      practiceRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else if (tab === 'assessments' && assessmentsRef.current) {
      assessmentsRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else if (tab === 'reflection' && reflectionRef.current) {
      reflectionRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Breadcrumb & Header with Language Switcher */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <Link to="/courses" className="inline-flex items-center gap-1 text-sm text-sky-700 hover:underline">
            <ChevronLeft className="h-4 w-4" />Courses
          </Link>
          <h1 className="mt-1 text-2xl font-bold text-navy">
            {language === 'ta' && (course.title.includes('Puzzle') || course.slug.includes('puzzle'))
              ? 'புதிர்கள் (Puzzles)'
              : language === 'ta' && (course.title.includes('Simplification') || course.slug.includes('simplification'))
              ? 'சுருக்குதல் (Simplification)'
              : language === 'ta' && (course.title.includes('Number') || course.slug.includes('number') || course.slug.includes('series'))
              ? 'எண் தொடர்கள் (Number Series)'
              : language === 'ta' && (course.title.includes('Logical') || course.slug.includes('logical'))
              ? 'தருக்கக் காரணவியல் (Logical Reasoning)'
              : language === 'ta' && (course.title.includes('Area') || course.slug.includes('area') || course.slug.includes('volume'))
              ? 'பரப்பளவு மற்றும் கன அளவு (Area and Volume)'
              : language === 'ta' && (course.title.includes('Time') || course.slug.includes('time'))
              ? 'காலம் மற்றும் வேலை (Time and Work)'
              : language === 'ta' && (course.title.includes('Ratio') || course.slug.includes('ratio'))
              ? 'விகிதம் மற்றும் விகிதசமம் (Ratio and Proportion)'
              : language === 'ta' && (course.title.includes('Percentage') || course.slug.includes('percent'))
              ? 'சதவீதம் (Percentage)'
              : course.title}
          </h1>
          {course.description && <p className="mt-1 max-w-3xl text-sm text-navy-600">{course.description}</p>}
        </div>

        {/* Language Selection Switcher */}
        <div className="flex items-center gap-1.5 self-start sm:self-auto rounded-xl bg-navy-50 p-1.5 border border-line shadow-xs">
          <span className="text-xs font-medium text-navy-500 px-2">Language:</span>
          <button
            type="button"
            onClick={() => handleLanguageChange('en')}
            className={`rounded-lg px-3 py-1.5 text-xs font-bold transition-all ${
              language === 'en'
                ? 'bg-sky-600 text-white shadow-sm'
                : 'text-navy-700 hover:bg-navy-200/60'
            }`}
          >
            🇬🇧 English
          </button>
          <button
            type="button"
            onClick={() => handleLanguageChange('ta')}
            className={`rounded-lg px-3 py-1.5 text-xs font-bold transition-all ${
              language === 'ta'
                ? 'bg-sky-600 text-white shadow-sm'
                : 'text-navy-700 hover:bg-navy-200/60'
            }`}
          >
            🇮🇳 தமிழ் (Tamil)
          </button>
        </div>
      </div>

      {/* Sequential Learning Path Navigator Bar (Material 3 Filter Chips) */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line pb-3">
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setActiveTab('all')}
            className={`inline-flex items-center gap-1.5 rounded-full px-3.5 py-2 text-xs font-semibold transition-all m3-touch min-h-[40px] ${
              activeTab === 'all'
                ? 'bg-navy-900 text-white shadow-xs'
                : 'bg-white border border-line text-navy-700 hover:bg-navy-50'
            }`}
          >
            <Layers className="h-4 w-4" />
            <span>Complete Flow</span>
          </button>

          <button
            type="button"
            onClick={() => scrollToSection('learn')}
            className={`inline-flex items-center gap-1.5 rounded-full px-3.5 py-2 text-xs font-semibold transition-all m3-touch min-h-[40px] ${
              activeTab === 'learn'
                ? 'bg-sky-600 text-white shadow-xs'
                : 'bg-white border border-line text-sky-800 hover:bg-sky-50'
            }`}
          >
            <BookOpen className="h-4 w-4" />
            <span>1. Learn</span>
          </button>

          <button
            type="button"
            onClick={() => scrollToSection('practice')}
            className={`inline-flex items-center gap-1.5 rounded-full px-3.5 py-2 text-xs font-semibold transition-all m3-touch min-h-[40px] ${
              activeTab === 'practice'
                ? 'bg-amber-600 text-white shadow-xs'
                : 'bg-white border border-line text-amber-900 hover:bg-amber-50'
            }`}
          >
            <Dumbbell className="h-4 w-4" />
            <span>2. Practice ({practice.length})</span>
          </button>

          <button
            type="button"
            onClick={() => scrollToSection('assessments')}
            className={`inline-flex items-center gap-1.5 rounded-full px-3.5 py-2 text-xs font-semibold transition-all m3-touch min-h-[40px] ${
              activeTab === 'assessments'
                ? 'bg-mint-700 text-white shadow-xs'
                : 'bg-white border border-line text-mint-900 hover:bg-mint-50'
            }`}
          >
            <Award className="h-4 w-4" />
            <span>3. Assessments ({graded.length})</span>
          </button>

          <button
            type="button"
            onClick={() => scrollToSection('reflection')}
            className={`inline-flex items-center gap-1.5 rounded-full px-3.5 py-2 text-xs font-semibold transition-all m3-touch min-h-[40px] ${
              activeTab === 'reflection'
                ? 'bg-purple-700 text-white shadow-xs'
                : 'bg-white border border-line text-purple-900 hover:bg-purple-50'
            }`}
          >
            <Sparkles className="h-4 w-4" />
            <span>{language === 'ta' ? '4. சிந்தனைச் செயல்பாடு' : '4. Reflection'}</span>
            {!allGradedCompleted && <Lock className="h-3 w-3 text-navy-400 opacity-70" />}
          </button>
        </div>
      </div>

      {/* ---------------------------------------------------- */}
      {/* 1. LEARN PART                                         */}
      {/* ---------------------------------------------------- */}
      {(activeTab === 'all' || activeTab === 'learn') && (
        <section ref={learnRef} className="space-y-3">
          <div className="flex items-center gap-2">
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-sky text-white text-xs font-bold">
              1
            </span>
            <div>
              <h2 className="text-lg font-bold text-navy flex items-center gap-2">
                Learn
                <span className="text-xs font-normal text-sky-700 bg-sky-50 px-2 py-0.5 rounded border border-sky-100">
                  Concept Guides & Formulas
                </span>
              </h2>
            </div>
          </div>
          <p className="text-sm text-navy-500">
            Study essential formulas, concepts, shortcut tricks, and model questions before starting your drills.
          </p>
          <CourseLearnSection
            assessments={items}
            courseTitle={course.title}
            courseSlug={course.slug}
            language={language}
            onGoToPractice={() => scrollToSection('practice')}
          />
        </section>
      )}

      {/* ---------------------------------------------------- */}
      {/* 2. PRACTICE PART                                      */}
      {/* ---------------------------------------------------- */}
      {(activeTab === 'all' || activeTab === 'practice') && (
        <section ref={practiceRef} className="space-y-3 pt-4 border-t border-line">
          <div className="flex items-center gap-2">
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-amber-500 text-white text-xs font-bold">
              2
            </span>
            <div>
              <h2 className="text-lg font-bold text-navy flex items-center gap-2">
                Practice
                <span className="text-xs font-normal text-amber-800 bg-amber-50 px-2 py-0.5 rounded border border-amber-100">
                  Untimed · Instant Feedback
                </span>
              </h2>
            </div>
          </div>
          <p className="text-sm text-navy-500">
            Practice at your own pace with no timers or camera proctoring. Explanations are shown after every question.
          </p>
          <div className="space-y-3">
            {practice.map((p) => (
              <AssessmentCard key={p.id} item={p} language={language} />
            ))}
            {practice.length === 0 && (
              <Card>
                <EmptyState
                  title="No practice sets currently available"
                  description="Practice modules for this course are being prepared. You can proceed directly to Assessments."
                />
              </Card>
            )}
          </div>
        </section>
      )}

      {/* ---------------------------------------------------- */}
      {/* 3. ASSESSMENTS PART                                   */}
      {/* ---------------------------------------------------- */}
      {(activeTab === 'all' || activeTab === 'assessments') && (
        <section ref={assessmentsRef} className="space-y-3 pt-4 border-t border-line">
          <div className="flex items-center gap-2">
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-mint-600 text-white text-xs font-bold">
              3
            </span>
            <div>
              <h2 className="text-lg font-bold text-navy flex items-center gap-2">
                Assessments
                <span className="text-xs font-normal text-mint-800 bg-mint-50 px-2 py-0.5 rounded border border-mint-100">
                  Graded · Proctored & Timed
                </span>
              </h2>
            </div>
          </div>
          <p className="text-sm text-navy-500">
            Proctored, timed, one attempt each. Pass each test to unlock the next test in the sequence.
          </p>
          <div className="space-y-3">
            {graded.map((g, i) => (
              <AssessmentCard
                key={g.id}
                item={g}
                language={language}
                previousTitle={i > 0 ? (language === 'ta' && graded[i - 1].title_ta ? graded[i - 1].title_ta! : graded[i - 1].title) : undefined}
              />
            ))}
            {graded.length === 0 && (
              <Card>
                <EmptyState title="No graded assessments available yet" />
              </Card>
            )}
          </div>
        </section>
      )}

      {/* ---------------------------------------------------- */}
      {/* 4. REFLECTIVE ACTIVITY PART                          */}
      {/* ---------------------------------------------------- */}
      {(activeTab === 'all' || activeTab === 'reflection') && (
        <section ref={reflectionRef} className="space-y-3 pt-4 border-t border-line">
          <div className="flex items-center gap-2">
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-purple-600 text-white text-xs font-bold">
              4
            </span>
            <div>
              <h2 className="text-lg font-bold text-navy flex items-center gap-2">
                {language === 'ta' ? '8. சிந்தனைச் செயல்பாடு' : 'Reflective Activity'}
                <span className="text-xs font-normal text-purple-800 bg-purple-50 px-2 py-0.5 rounded border border-purple-100">
                  {language === 'ta' ? 'சுய மதிப்பீடு' : 'Self-Assessment & Metacognition'}
                </span>
              </h2>
            </div>
          </div>
          <p className="text-sm text-navy-500">
            {language === 'ta'
              ? 'இப்பாடத்தை நிறைவு செய்த பின், பின்வரும் வினாக்களைப் பற்றிச் சிந்திக்கவும்.'
              : 'Reflect on the problem-solving strategies, challenging patterns, and personal confidence gained from this lesson.'}
          </p>
          <CourseReflectiveActivity
            courseSlug={course.slug}
            courseTitle={course.title}
            language={language}
            isAssessmentLocked={!allGradedCompleted}
            onGoToAssessments={() => scrollToSection('assessments')}
          />
        </section>
      )}
    </div>
  );
}
