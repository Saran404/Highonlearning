import { Sparkles, User as UserIcon, BookOpen, Calendar, CheckCircle2, Search, RefreshCw, ChevronRight } from 'lucide-react';
import { useCallback, useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { adminApi } from '../../api/admin';
import { toApiError } from '../../api/client';
import type { AdminUserReflectionSummary, UserCourseReflection } from '../../types';
import Button from '../common/Button';
import Card from '../common/Card';
import EmptyState from '../common/EmptyState';
import { formatDate } from '../../utils/format';

export default function AdminReflectionSection() {
  const [summaries, setSummaries] = useState<AdminUserReflectionSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const [selectedCourseSlug, setSelectedCourseSlug] = useState<string | null>(null);

  const loadData = useCallback(() => {
    setLoading(true);
    adminApi
      .reflections(search)
      .then((data) => {
        setSummaries(data);
        if (data.length > 0) {
          // If no user selected or currently selected user not in data, pick the first
          if (!selectedUserId || !data.some((u) => u.user_id === selectedUserId)) {
            setSelectedUserId(data[0].user_id);
            if (data[0].courses.length > 0) {
              setSelectedCourseSlug(data[0].courses[0].course_slug);
            }
          }
        } else {
          setSelectedUserId(null);
          setSelectedCourseSlug(null);
        }
      })
      .catch((e) => toast.error(toApiError(e).message))
      .finally(() => setLoading(false));
  }, [search, selectedUserId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const selectedUser = summaries.find((u) => u.user_id === selectedUserId);

  // When selected user changes, adjust selectedCourseSlug if needed
  useEffect(() => {
    if (selectedUser && selectedUser.courses.length > 0) {
      if (!selectedCourseSlug || !selectedUser.courses.some((c) => c.course_slug === selectedCourseSlug)) {
        setSelectedCourseSlug(selectedUser.courses[0].course_slug);
      }
    }
  }, [selectedUser, selectedCourseSlug]);

  const selectedCourse: UserCourseReflection | undefined = selectedUser?.courses.find(
    (c) => c.course_slug === selectedCourseSlug
  ) ?? selectedUser?.courses[0];

  return (
    <div className="space-y-4">
      {/* Top Filter and Search Bar */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-xl font-bold text-navy flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-purple-600" />
            Reflection Activity
          </h2>
          <p className="text-sm text-navy-500">
            Review self-reflection and metacognitive feedback submitted by students across all courses.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-navy-400" />
            <input
              type="text"
              placeholder="Search student or email..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="field !py-1.5 !pl-9 !w-64 text-sm"
              aria-label="Search reflection submissions"
            />
          </div>
          <Button
            size="sm"
            variant="secondary"
            onClick={loadData}
            icon={<RefreshCw className="h-4 w-4" />}
            aria-label="Refresh reflections"
          />
        </div>
      </div>

      {loading ? (
        <Card className="p-8 text-center">
          <div className="inline-flex items-center gap-3 text-sm text-navy-500">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-navy-300 border-t-purple-600" />
            <span>Loading reflection activities...</span>
          </div>
        </Card>
      ) : summaries.length === 0 ? (
        <Card>
          <EmptyState
            title="No reflection submissions yet"
            description="When students complete the reflective activity at the end of a course, their responses will be listed here."
          />
        </Card>
      ) : (
        <div className="grid gap-5 lg:grid-cols-12 items-start">
          {/* Left Column: Students List */}
          <div className="lg:col-span-5 space-y-2">
            <div className="rounded-xl border border-line bg-white shadow-xs overflow-hidden">
              <div className="border-b border-line bg-navy-50/60 px-4 py-2.5 flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-navy-600">
                  Students ({summaries.length})
                </span>
                <span className="text-xs text-navy-400">Click a student to view answers</span>
              </div>

              <div className="divide-y divide-line max-h-[36rem] overflow-y-auto">
                {summaries.map((u) => {
                  const isSelected = u.user_id === selectedUserId;
                  return (
                    <button
                      key={u.user_id}
                      type="button"
                      onClick={() => {
                        setSelectedUserId(u.user_id);
                        if (u.courses.length > 0) {
                          setSelectedCourseSlug(u.courses[0].course_slug);
                        }
                      }}
                      className={`w-full flex items-center justify-between p-3.5 text-left transition-colors cursor-pointer ${
                        isSelected
                          ? 'bg-purple-50/80 border-l-4 border-purple-600'
                          : 'hover:bg-navy-50/60'
                      }`}
                    >
                      <div className="flex items-center gap-3 min-w-0 flex-1">
                        <div
                          className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl font-bold text-xs uppercase ${
                            isSelected
                              ? 'bg-purple-600 text-white shadow-2xs'
                              : 'bg-navy-100 text-navy-700'
                          }`}
                        >
                          {u.name.charAt(0) || <UserIcon className="h-4 w-4" />}
                        </div>
                        <div className="min-w-0 flex-1">
                          <div className="truncate font-semibold text-navy text-sm">{u.name}</div>
                          <div className="truncate text-xs text-navy-400">{u.email}</div>
                          <div className="mt-1 flex items-center gap-2 text-[11px] text-navy-500">
                            <span className="inline-flex items-center gap-1 font-medium text-purple-700 bg-purple-100/70 px-1.5 py-0.2 rounded">
                              <BookOpen className="h-3 w-3" />
                              {u.total_reflections} {u.total_reflections === 1 ? 'course' : 'courses'}
                            </span>
                            {u.latest_submitted_at && (
                              <span className="truncate">
                                {formatDate(u.latest_submitted_at, 'MMM d, yyyy')}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>

                      <ChevronRight
                        className={`h-4 w-4 shrink-0 transition-transform ${
                          isSelected ? 'text-purple-600 translate-x-0.5' : 'text-navy-300'
                        }`}
                      />
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Right Column: User's Course Reflections & Answers */}
          <div className="lg:col-span-7 space-y-4">
            {selectedUser && selectedCourse ? (
              <div className="space-y-4">
                {/* User Header Card */}
                <div className="rounded-2xl border border-line bg-gradient-to-r from-purple-50/50 via-white to-sky-50/30 p-5 shadow-xs">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold uppercase tracking-wider text-purple-700 bg-purple-100 px-2 py-0.5 rounded-md">
                          Student Reflection
                        </span>
                        <span className="text-xs text-navy-400">ID #{selectedUser.user_id}</span>
                      </div>
                      <h3 className="mt-1 text-lg font-bold text-navy">{selectedUser.name}</h3>
                      <p className="text-xs text-navy-500">{selectedUser.email}</p>
                    </div>

                    <div className="text-left sm:text-right">
                      <span className="text-xs text-navy-400 block">Total Completed</span>
                      <span className="text-sm font-bold text-navy">
                        {selectedUser.total_reflections}{' '}
                        {selectedUser.total_reflections === 1 ? 'Course' : 'Courses'}
                      </span>
                    </div>
                  </div>

                  {/* Course Selector Tabs */}
                  {selectedUser.courses.length > 1 && (
                    <div className="mt-4 pt-3 border-t border-line">
                      <div className="text-xs font-bold uppercase tracking-wider text-navy-500 mb-2">
                        Select Course:
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {selectedUser.courses.map((c) => {
                          const active = c.course_slug === selectedCourse.course_slug;
                          return (
                            <button
                              key={c.course_id}
                              type="button"
                              onClick={() => setSelectedCourseSlug(c.course_slug)}
                              className={`inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition-all cursor-pointer ${
                                active
                                  ? 'bg-purple-700 text-white shadow-xs'
                                  : 'bg-white border border-line text-navy-700 hover:bg-navy-50'
                              }`}
                            >
                              <BookOpen className="h-3.5 w-3.5" />
                              <span>{c.course_title}</span>
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </div>

                {/* Selected Course Reflection Card */}
                <Card className="p-5 space-y-4">
                  <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line pb-3">
                    <div>
                      <span className="text-xs font-bold text-purple-700 uppercase tracking-wider">
                        Course
                      </span>
                      <h4 className="text-base font-bold text-navy">{selectedCourse.course_title}</h4>
                    </div>

                    <div className="flex items-center gap-1.5 text-xs text-navy-500 bg-navy-50 border border-line px-2.5 py-1 rounded-lg">
                      <Calendar className="h-3.5 w-3.5 text-navy-400" />
                      <span>Submitted: {formatDate(selectedCourse.submitted_at, 'MMM d, yyyy · h:mm a')}</span>
                    </div>
                  </div>

                  {/* Reflection Answers List */}
                  <div className="space-y-3.5">
                    {selectedCourse.answers.map((ans, idx) => (
                      <div
                        key={idx}
                        className="rounded-xl border border-line bg-white p-4 shadow-2xs hover:border-purple-200 transition-colors"
                      >
                        <div className="flex items-start gap-3">
                          <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-md bg-purple-100 text-purple-800 text-xs font-bold">
                            {ans.question_number || idx + 1}
                          </span>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-semibold text-navy leading-relaxed">
                              {ans.question}
                            </p>

                            <div className="mt-2.5 rounded-lg border border-purple-200 bg-purple-50/70 p-3 flex items-start gap-2.5">
                              <CheckCircle2 className="h-4 w-4 shrink-0 text-purple-600 mt-0.5" />
                              <div>
                                <span className="text-xs font-bold uppercase tracking-wider text-purple-800 block mb-0.5">
                                  Selected Response
                                </span>
                                <span className="text-sm font-medium text-navy-900 leading-normal">
                                  {ans.selected_option}
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}

                    {selectedCourse.answers.length === 0 && (
                      <p className="py-6 text-center text-sm text-navy-400">
                        No answers recorded for this course.
                      </p>
                    )}
                  </div>
                </Card>
              </div>
            ) : (
              <Card className="p-8 text-center">
                <p className="text-sm text-navy-400">Select a student on the left to view their reflection answers.</p>
              </Card>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
