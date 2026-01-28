"use client";

import { useState } from "react";
import {
  STEP_1_CORE_STRUGGLES,
  STEP_2_FOCUS_AREAS,
  STEP_3_ROOT_CAUSES,
  WizardOption,
} from "@/lib/wizard-data";

interface WizardSelection {
  step1: string | null;
  step2: string | null;
  step3: string | null;
  customContext: string;
}

interface Props {
  onComplete: (context: string, selections: WizardSelection) => void;
  onQuickSearch: () => void;
}

export default function ProblemWizard({ onComplete, onQuickSearch }: Props) {
  const [currentStep, setCurrentStep] = useState(1);
  const [selections, setSelections] = useState<WizardSelection>({
    step1: null,
    step2: null,
    step3: null,
    customContext: "",
  });
  const [customContext, setCustomContext] = useState("");

  const handleSelect = (step: number, value: string) => {
    const newSelections = { ...selections };

    if (step === 1) {
      newSelections.step1 = value;
      newSelections.step2 = null;
      newSelections.step3 = null;
    } else if (step === 2) {
      newSelections.step2 = value;
      newSelections.step3 = null;
    } else if (step === 3) {
      newSelections.step3 = value;
    }

    setSelections(newSelections);
    setCurrentStep(step + 1);
  };

  const handleSubmit = () => {
    const step1Option = STEP_1_CORE_STRUGGLES.options.find((o) => o.id === selections.step1);
    const step2Options = selections.step1 ? STEP_2_FOCUS_AREAS[selections.step1]?.options : [];
    const step2Option = step2Options?.find((o) => o.id === selections.step2);
    const step3Options = selections.step2 ? STEP_3_ROOT_CAUSES[selections.step2]?.options : [];
    const step3Option = step3Options?.find((o) => o.id === selections.step3);

    let context = `My main challenge: ${step1Option?.label || ""}.`;
    context += ` Specifically: ${step2Option?.label || ""}.`;
    context += ` The root issue: ${step3Option?.label || ""} - ${step3Option?.description || ""}.`;

    if (customContext.trim()) {
      context += ` Additional details: ${customContext}`;
    }

    const finalSelections = { ...selections, customContext };
    onComplete(context, finalSelections);
  };

  const goBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const getStepInfo = () => {
    switch (currentStep) {
      case 1:
        return { title: STEP_1_CORE_STRUGGLES.title, subtitle: STEP_1_CORE_STRUGGLES.subtitle };
      case 2:
        return selections.step1 && STEP_2_FOCUS_AREAS[selections.step1]
          ? { title: STEP_2_FOCUS_AREAS[selections.step1].title, subtitle: STEP_2_FOCUS_AREAS[selections.step1].subtitle }
          : { title: "", subtitle: "" };
      case 3:
        return selections.step2 && STEP_3_ROOT_CAUSES[selections.step2]
          ? { title: STEP_3_ROOT_CAUSES[selections.step2].title, subtitle: STEP_3_ROOT_CAUSES[selections.step2].subtitle }
          : { title: "", subtitle: "" };
      case 4:
        return { title: "Anything else we should know?", subtitle: "Optional but helps us find better matches" };
      default:
        return { title: "", subtitle: "" };
    }
  };

  const renderProgressBar = () => (
    <div className="flex items-center justify-center mb-10">
      <div className="flex items-center bg-gray-100 rounded-full px-4 py-2">
        {[1, 2, 3, 4].map((step) => (
          <div key={step} className="flex items-center">
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all duration-300 ${
                step < currentStep
                  ? "bg-emerald-500 text-white"
                  : step === currentStep
                  ? "bg-kale text-white"
                  : "bg-white text-gray-400 border border-gray-200"
              }`}
            >
              {step < currentStep ? "✓" : step}
            </div>
            {step < 4 && (
              <div
                className={`w-8 h-0.5 mx-1 transition-all duration-300 ${
                  step < currentStep ? "bg-emerald-500" : "bg-gray-200"
                }`}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );

  const renderBreadcrumbs = () => {
    if (currentStep === 1) return null;

    const crumbs = [];
    if (selections.step1) {
      const opt = STEP_1_CORE_STRUGGLES.options.find((o) => o.id === selections.step1);
      if (opt) crumbs.push({ icon: opt.icon, label: opt.label });
    }
    if (selections.step2 && selections.step1) {
      const opt = STEP_2_FOCUS_AREAS[selections.step1]?.options.find((o) => o.id === selections.step2);
      if (opt) crumbs.push({ icon: opt.icon, label: opt.label });
    }
    if (selections.step3 && selections.step2) {
      const opt = STEP_3_ROOT_CAUSES[selections.step2]?.options.find((o) => o.id === selections.step3);
      if (opt) crumbs.push({ icon: opt.icon, label: opt.label });
    }

    return (
      <div className="mb-8 flex flex-wrap items-center justify-center gap-2 text-sm">
        {crumbs.map((crumb, idx) => (
          <span key={idx} className="flex items-center">
            {idx > 0 && <span className="text-gray-300 mx-2">→</span>}
            <span className="bg-kale-50 text-kale px-3 py-1.5 rounded-full flex items-center gap-1.5">
              <span>{crumb.icon}</span>
              <span className="font-medium">{crumb.label}</span>
            </span>
          </span>
        ))}
      </div>
    );
  };

  const renderOptions = (options: WizardOption[], step: number) => (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 animate-fade-in">
      {options.map((option) => (
        <button
          key={option.id}
          onClick={() => handleSelect(step, option.id)}
          className="card p-5 text-left group cursor-pointer hover:scale-[1.02] active:scale-[0.98] transition-all focus:outline-none focus:ring-2 focus:ring-kale focus:ring-offset-2 hover:border-kale/30"
          tabIndex={0}
          aria-label={`${option.label}: ${option.description}`}
        >
          <div className="flex items-start gap-4">
            <span className="text-2xl group-hover:scale-110 transition-transform">{option.icon}</span>
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-gray-900 group-hover:text-kale transition-colors leading-tight">
                {option.label}
              </h3>
              <p className="text-gray-500 text-sm mt-1 leading-snug">
                {option.description}
              </p>
            </div>
            <svg
              className="w-5 h-5 text-gray-300 group-hover:text-kale group-hover:translate-x-1 transition-all flex-shrink-0 mt-1"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </button>
      ))}
    </div>
  );

  const renderContextStep = () => (
    <div className="animate-fade-in max-w-lg mx-auto">
      <div className="card p-6 mb-6">
        <textarea
          value={customContext}
          onChange={(e) => setCustomContext(e.target.value)}
          placeholder="Example: 2 years in the business, about 8 deals a year, works mostly with first-time buyers, spouse is getting frustrated with the hours..."
          rows={4}
          className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-kale focus:ring-2 focus:ring-kale/10 transition resize-none text-gray-900 placeholder-gray-400 text-base"
        />
      </div>

      <button
        onClick={handleSubmit}
        className="btn-primary w-full text-lg flex items-center justify-center gap-2 mb-4"
      >
        <span>Find Episodes</span>
        <span>→</span>
      </button>

      <button
        onClick={() => {
          setCustomContext("");
          handleSubmit();
        }}
        className="w-full text-gray-400 hover:text-kale transition text-sm py-2"
      >
        Skip and search now
      </button>
    </div>
  );

  const { title, subtitle } = getStepInfo();

  return (
    <div className="max-w-2xl mx-auto px-4">
      {renderProgressBar()}

      {/* Quick search option for power users - More visible */}
      {currentStep === 1 && (
        <div className="text-center mb-8">
          <button
            onClick={onQuickSearch}
            className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-kale bg-gray-100 hover:bg-kale-50 px-4 py-2 rounded-full transition group"
          >
            <span>Know what you're looking for?</span>
            <span className="font-medium text-kale group-hover:underline">Type directly →</span>
          </button>
        </div>
      )}

      {currentStep > 1 && (
        <button
          onClick={goBack}
          className="mb-6 text-gray-400 hover:text-kale flex items-center gap-2 transition text-sm font-medium"
        >
          <span>←</span>
          <span>Back</span>
        </button>
      )}

      {renderBreadcrumbs()}

      <div className="mb-8 text-center">
        <h2 className="text-2xl sm:text-3xl font-semibold text-gray-900 mb-2">
          {title}
        </h2>
        <p className="text-gray-500">{subtitle}</p>
      </div>

      {currentStep === 1 && renderOptions(STEP_1_CORE_STRUGGLES.options, 1)}

      {currentStep === 2 &&
        selections.step1 &&
        STEP_2_FOCUS_AREAS[selections.step1] &&
        renderOptions(STEP_2_FOCUS_AREAS[selections.step1].options, 2)}

      {currentStep === 3 &&
        selections.step2 &&
        STEP_3_ROOT_CAUSES[selections.step2] &&
        renderOptions(STEP_3_ROOT_CAUSES[selections.step2].options, 3)}

      {currentStep === 4 && renderContextStep()}
    </div>
  );
}
