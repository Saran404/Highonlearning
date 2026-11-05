import type { ReactNode } from 'react';
import BrandLogo from '../common/BrandLogo';

export default function AuthShell({ title, subtitle, children, footer }: { title: string; subtitle: string; children: ReactNode; footer: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col lg:flex-row">
      <div className="flex flex-col justify-between bg-navy px-6 py-8 text-white lg:w-2/5 lg:px-12 lg:py-12">
        <BrandLogo to="/" size="md" showTagline onDark />
        <div className="my-8 hidden lg:block">
          <p className="max-w-sm text-3xl font-semibold leading-tight">Practise like it's the exam hall.</p>
          <p className="mt-3 max-w-sm text-navy-200">Timed, proctored tests for TNPSC, SSC, Banking, UPSC, RRB and IBPS — with full solutions and your rank.</p>
        </div>
        <p className="hidden text-xs text-navy-300 lg:block">One account works on one device at a time, so nobody else can sit your test.</p>
      </div>
      <main className="flex flex-1 items-center justify-center px-4 py-10">
        <div className="w-full max-w-sm">
          <h1 className="text-2xl">{title}</h1>
          <p className="mt-1 text-sm text-navy-500">{subtitle}</p>
          <div className="mt-6">{children}</div>
          <p className="mt-6 text-center text-sm text-navy-500">{footer}</p>
        </div>
      </main>
    </div>
  );
}
