import { CheckCircle2, Check, Sparkles, Send, RotateCcw, AlertCircle, HelpCircle, Lock, ArrowRight } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { coursesApi } from '../../api/courses';
import { toApiError } from '../../api/client';
import Button from '../common/Button';
import Card from '../common/Card';
import type { ReflectionAnswerItem } from '../../types';
import { formatDate } from '../../utils/format';
import { getCourseReflectionQuestions } from '../../utils/reflectionData';
import { useCourseStore } from '../../store/courseStore';

interface Props {
  courseSlug: string;
  courseTitle: string;
  language?: 'en' | 'ta';
  isAssessmentLocked?: boolean;
  onGoToAssessments?: () => void;
}

export default function CourseReflectiveActivity({
  courseSlug,
  courseTitle,
  language = 'en',
  isAssessmentLocked = false,
  onGoToAssessments,
}: Props) {
  const isTa = language === 'ta';
  const questions = getCourseReflectionQuestions(courseSlug, courseTitle);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [submittedAt, setSubmittedAt] = useState<string | null>(null);
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [isEditing, setIsEditing] = useState<boolean>(false);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    coursesApi
      .reflection(courseSlug)
      .then((res) => {
        if (cancelled) return;
        if (res.submitted && res.answers.length > 0) {
          const map: Record<number, string> = {};
          res.answers.forEach((a) => {
            map[a.question_number] = a.selected_option;
          });
          setSelectedAnswers(map);
          setIsSubmitted(true);
          setSubmittedAt(res.submitted_at ?? null);
        } else {
          setIsSubmitted(false);
          setSelectedAnswers({});
        }
      })
      .catch(() => {
        /* Not submitted or network error */
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [courseSlug]);

  const handleSelectOption = (qNumber: number, option: string) => {
    if (isSubmitted && !isEditing) return;
    setSelectedAnswers((prev) => ({
      ...prev,
      [qNumber]: option,
    }));
  };

  const answeredCount = Object.keys(selectedAnswers).length;
  const isComplete = answeredCount === questions.length;

  const handleSubmit = async () => {
    if (!isComplete) {
      toast.error(
        isTa
          ? `சமர்ப்பிக்கும் முன் அனைத்து ${questions.length} வினாக்களுக்கும் பதிலளிக்கவும்.`
          : `Please answer all ${questions.length} questions before submitting.`
      );
      return;
    }

    const payload: ReflectionAnswerItem[] = questions.map((q) => {
      const qText = isTa && q.question_ta ? q.question_ta : q.question;
      return {
        question_number: q.number,
        question: qText,
        selected_option: selectedAnswers[q.number] || '',
      };
    });

    setSubmitting(true);
    try {
      const res = await coursesApi.submitReflection(courseSlug, payload);
      setIsSubmitted(true);
      setIsEditing(false);
      setSubmittedAt(res.submitted_at ?? new Date().toISOString());

      // Mark course completed in store and reload courses so next course unlocks
      useCourseStore.getState().markCourseCompleted(courseSlug);
      useCourseStore.getState().fetchCourses().catch(() => {});

      toast.success(
        isTa
          ? '🎉 சிந்தனைச் செயல்பாடு நிறைவுற்றது! அடுத்த பாடம் திறக்கப்பட்டது.'
          : '🎉 Reflective activity complete! The next course is now unlocked.'
      );
    } catch (err) {
      toast.error(toApiError(err).message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <Card className="p-6">
        <div className="flex items-center gap-3 text-sm text-navy-500">
          <div className="h-4 w-4 animate-spin rounded-full border-2 border-navy-300 border-t-navy-700" />
          <span>{isTa ? 'சிந்தனைச் செயல்பாடு ஏற்றப்படுகிறது...' : 'Loading reflection activity...'}</span>
        </div>
      </Card>
    );
  }

  if (isAssessmentLocked && !isSubmitted) {
    return (
      <Card className="p-8 text-center border-dashed border-2 border-navy-200 bg-navy-50/40 shadow-xs">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-100 text-amber-700 shadow-2xs mb-3">
          <Lock className="h-6 w-6" />
        </div>
        <h3 className="text-base font-bold text-navy">
          {isTa ? 'சிந்தனைச் செயல்பாடு பூட்டப்பட்டுள்ளது' : 'Reflective Activity Locked'}
        </h3>
        <p className="mt-1.5 text-xs text-navy-600 sm:text-sm max-w-lg mx-auto">
          {isTa
            ? 'இப்பாடத்தின் அனைத்து மதிப்பிடப்பட்ட தேர்வுகளையும் நிறைவு செய்த பின்பே சிந்தனைச் செயல்பாடு திறக்கப்படும். சிந்தனைச் செயல்பாட்டை முடித்ததும் அடுத்த பாடம் திறக்கப்படும்!'
            : 'Complete all graded assessments in this course to unlock the Reflective Activity. Completing this reflection will unlock the next course in the sequence!'}
        </p>
        {onGoToAssessments && (
          <div className="mt-4">
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={onGoToAssessments}
              className="inline-flex items-center gap-1.5 text-xs font-semibold"
            >
              <span>{isTa ? 'மதிப்பீடுகளுக்குச் செல்' : 'Go to Graded Assessments'}</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          </div>
        )}
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {/* Course Completion & Next Course Unlock Celebration Banner */}
      {isSubmitted && (
        <div className="rounded-xl border border-mint-200 bg-gradient-to-r from-mint-50 via-white to-mint-50/60 p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-2xs">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-mint-600 text-white shadow-2xs">
              <CheckCircle2 className="h-5 w-5" />
            </div>
            <div>
              <p className="text-xs sm:text-sm font-bold text-mint-950">
                {isTa ? 'சிந்தனைச் செயல்பாடு நிறைவுற்றது — பாடம் நிறைவு!' : 'Reflective Activity Completed — Course Unlocked!'}
              </p>
              <p className="text-xs text-mint-800">
                {isTa
                  ? 'உங்கள் கற்றல் அனுபவம் பதிவு செய்யப்பட்டது. அடுத்த பாடம் திறக்கப்பட்டுள்ளது!'
                  : 'Your reflection has been recorded. The next course in your learning path is now unlocked!'}
              </p>
            </div>
          </div>
          <Link
            to="/courses"
            className="inline-flex items-center gap-1.5 text-xs font-bold text-mint-900 bg-white border border-mint-300 rounded-lg px-3.5 py-2 hover:bg-mint-100/50 shadow-2xs transition-colors shrink-0"
          >
            <span>{isTa ? 'பாடங்களின் பட்டியல்' : 'View Course Catalog'}</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>
      )}

      {/* Instructions Banner */}
      <div className="rounded-2xl border border-sky-100 bg-gradient-to-r from-sky-50 via-white to-sky-50/50 p-5 shadow-xs">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-start gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-sky-100 text-sky-700">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider text-sky-800 bg-sky-100/70 px-2 py-0.5 rounded-md">
                  {isTa ? 'சிந்தனைச் செயல்பாடு' : 'Reflection'}
                </span>
                {isSubmitted && (
                  <span className="inline-flex items-center gap-1 text-xs font-semibold text-mint-700 bg-mint-50 px-2 py-0.5 rounded-md border border-mint-200">
                    <CheckCircle2 className="h-3.5 w-3.5" /> {isTa ? 'நிறைவுற்றது' : 'Completed'}
                  </span>
                )}
              </div>
              <h3 className="mt-1 text-base font-bold text-navy">
                {isTa ? `8. சிந்தனைச் செயல்பாடு` : `Reflective Activity: ${courseTitle}`}
              </h3>
              <p className="mt-0.5 text-xs text-navy-600 sm:text-sm">
                {isTa
                  ? 'இப்பாடத்தை நிறைவு செய்த பின், பின்வரும் வினாக்களைப் பற்றிச் சிந்திக்கவும். அறிவுறுத்தல்: ஒவ்வொரு கூற்றையும் கவனமாகப் படித்து, உங்கள் கற்றல் அனுபவத்தைச் சிறப்பாகப் பிரதிபலிக்கும் விருப்பத்தைத் தேர்ந்தெடுக்கவும்.'
                  : 'Instructions: Read each statement carefully and select the option that best reflects your learning experience.'}
              </p>
            </div>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <span className="rounded-full bg-white border border-line px-3 py-1 text-xs font-bold tabular-nums text-navy-700 shadow-2xs">
              {answeredCount} / {questions.length} {isTa ? 'பதிலளிக்கப்பட்டது' : 'answered'}
            </span>
          </div>
        </div>

        {/* Progress bar */}
        <div className="mt-3.5 h-1.5 w-full overflow-hidden rounded-full bg-navy-100">
          <div
            className="h-full bg-sky transition-all duration-300 rounded-full"
            style={{ width: `${(answeredCount / questions.length) * 100}%` }}
          />
        </div>

        {isSubmitted && submittedAt && !isEditing && (
          <div className="mt-3 flex flex-wrap items-center justify-between gap-2 border-t border-sky-100 pt-3 text-xs text-navy-500">
            <span>
              {isTa
                ? `${formatDate(submittedAt, 'MMM d, yyyy · h:mm a')} அன்று சமர்ப்பிக்கப்பட்டது`
                : `Submitted on ${formatDate(submittedAt, 'MMM d, yyyy · h:mm a')}`}
            </span>
            <button
              type="button"
              onClick={() => setIsEditing(true)}
              className="font-semibold text-sky-700 hover:text-sky-900 hover:underline flex items-center gap-1"
            >
              <RotateCcw className="h-3.5 w-3.5" /> {isTa ? 'பதில்களை மாற்றுக' : 'Modify responses'}
            </button>
          </div>
        )}
      </div>

      {/* Question Cards List */}
      <div className="space-y-4">
        {questions.map((q) => {
          const currentAnswer = selectedAnswers[q.number];
          const isAnswered = Boolean(currentAnswer);
          const qText = isTa && q.question_ta ? q.question_ta : q.question;
          const options = isTa && q.options_ta && q.options_ta.length === q.options.length ? q.options_ta : q.options;

          return (
            <Card key={q.number} className="overflow-hidden p-5 transition-shadow hover:shadow-xs">
              <div className="flex items-start gap-3">
                <span
                  className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-lg text-xs font-bold transition-colors ${
                    isAnswered
                      ? 'bg-sky text-white shadow-2xs'
                      : 'bg-navy-100 text-navy-600'
                  }`}
                >
                  {q.number}
                </span>
                <div className="flex-1">
                  <h4 className="text-sm font-semibold text-navy leading-relaxed sm:text-base">
                    {qText}
                  </h4>

                  {/* Options */}
                  <div className="mt-3.5 grid gap-2 sm:grid-cols-1">
                    {options.map((optText, optIndex) => {
                      const canonicalEnglishOpt = q.options[optIndex];
                      const canonicalTamilOpt = q.options_ta?.[optIndex];
                      const isSelected =
                        currentAnswer === optText ||
                        currentAnswer === canonicalEnglishOpt ||
                        (canonicalTamilOpt && currentAnswer === canonicalTamilOpt);
                      const disabled = isSubmitted && !isEditing;

                      return (
                        <button
                          key={optIndex}
                          type="button"
                          disabled={disabled}
                          onClick={() => handleSelectOption(q.number, optText)}
                          className={`group flex items-center justify-between rounded-xl border p-3 text-left transition-all ${
                            isSelected
                              ? 'border-sky-500 bg-sky-50/70 text-navy-900 font-medium shadow-2xs'
                              : disabled
                              ? 'border-line bg-navy-50/40 text-navy-500 opacity-80 cursor-not-allowed'
                              : 'border-line bg-white text-navy-700 hover:border-navy-300 hover:bg-navy-50/50 cursor-pointer'
                          }`}
                        >
                          <div className="flex items-center gap-3 pr-2">
                            <span
                              className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border text-[11px] transition-colors ${
                                isSelected
                                  ? 'border-sky bg-sky text-white'
                                  : 'border-navy-300 bg-white group-hover:border-navy-400'
                              }`}
                            >
                              {isSelected ? <Check className="h-3 w-3 stroke-[3]" /> : null}
                            </span>
                            <span className="text-xs sm:text-sm leading-normal">{optText}</span>
                          </div>
                          {isSelected && (
                            <span className="shrink-0 text-xs font-semibold text-sky-700 hidden sm:inline">
                              {isTa ? 'தேர்ந்தெடுக்கப்பட்டது' : 'Selected'}
                            </span>
                          )}
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Submission Actions */}
      {(!isSubmitted || isEditing) && (
        <div className="sticky bottom-4 z-10 flex items-center justify-between gap-3 rounded-2xl border border-line bg-white/95 p-4 shadow-lg backdrop-blur-md">
          <div className="flex items-center gap-2">
            {!isComplete ? (
              <span className="flex items-center gap-1.5 text-xs text-amber-700 font-medium bg-amber-50 px-2.5 py-1 rounded-lg border border-amber-200">
                <AlertCircle className="h-3.5 w-3.5 shrink-0" />
                {isTa
                  ? `அனைத்து ${questions.length} வினாக்களுக்கும் பதிலளிக்கவும்`
                  : `Select an option for all ${questions.length} statements`}
              </span>
            ) : (
              <span className="flex items-center gap-1.5 text-xs text-mint-700 font-medium bg-mint-50 px-2.5 py-1 rounded-lg border border-mint-200">
                <CheckCircle2 className="h-3.5 w-3.5 shrink-0" />
                {isTa ? 'அனைத்து வினாக்களுக்கும் பதிலளிக்கப்பட்டது' : 'All statements answered'}
              </span>
            )}
          </div>

          <div className="flex items-center gap-2">
            {isEditing && (
              <Button
                variant="secondary"
                size="md"
                onClick={() => setIsEditing(false)}
                disabled={submitting}
              >
                {isTa ? 'ரத்து' : 'Cancel'}
              </Button>
            )}
            <Button
              variant="primary"
              size="md"
              loading={submitting}
              disabled={!isComplete}
              onClick={handleSubmit}
              icon={<Send className="h-4 w-4" />}
            >
              {isSubmitted
                ? isTa
                  ? 'சிந்தனையைப் புதுப்பிக்கவும்'
                  : 'Update Reflection'
                : isTa
                ? 'சிந்தனையைச் சமர்ப்பிக்கவும்'
                : 'Submit Reflection'}
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
