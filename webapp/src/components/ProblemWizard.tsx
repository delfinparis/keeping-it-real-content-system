"use client";

import { useState, useEffect } from "react";
import {
  STEP_1_CORE_STRUGGLES,
  STEP_2_FOCUS_AREAS,
  STEP_3_ROOT_CAUSES,
  ROOT_CAUSE_TO_CATEGORIES,
  ROOT_CAUSE_KEYWORDS,
  WizardOption,
} from "@/lib/wizard-data";

interface ProblemOption {
  problem: string;
  episodes: number;
  category: string;
}

interface WizardSelection {
  step1: string | null;
  step2: string | null;
  step3: string | null;
  step4: string | null;
  step5: string;
}

interface Props {
  onComplete: (context: string, selections: WizardSelection) => void;
  problemMap: { [category: string]: { [problem: string]: any[] } };
}

export default function ProblemWizard({ onComplete, problemMap }: Props) {
  const [currentStep, setCurrentStep] = useState(1);
  const [selections, setSelections] = useState<WizardSelection>({
    step1: null,
    step2: null,
    step3: null,
    step4: null,
    step5: "",
  });
  const [step4Problems, setStep4Problems] = useState<ProblemOption[]>([]);
  const [customContext, setCustomContext] = useState("");

  // Get Step 4 problems based on Step 3 selection
  useEffect(() => {
    if (selections.step3) {
      const categories = ROOT_CAUSE_TO_CATEGORIES[selections.step3] || [];
      const keywords = ROOT_CAUSE_KEYWORDS[selections.step3] || [];

      const problems: ProblemOption[] = [];

      categories.forEach((category) => {
        if (problemMap[category]) {
          Object.entries(problemMap[category]).forEach(([problem, episodes]) => {
            const problemLower = problem.toLowerCase();
            const matchesKeyword =
              keywords.length === 0 ||
              keywords.some((kw) => problemLower.includes(kw.toLowerCase()));

            if (matchesKeyword) {
              problems.push({
                problem,
                episodes: Array.isArray(episodes) ? episodes.length : 0,
                category,
              });
            }
          });
        }
      });

      problems.sort((a, b) => b.episodes - a.episodes);
      setStep4Problems(problems.slice(0, 6));
    }
  }, [selections.step3, problemMap]);

  const handleSelect = (step: number, value: string) => {
    const newSelections = { ...selections };

    if (step === 1) {
      newSelections.step1 = value;
      newSelections.step2 = null;
      newSelections.step3 = null;
      newSelections.step4 = null;
    } else if (step === 2) {
      newSelections.step2 = value;
      newSelections.step3 = null;
      newSelections.step4 = null;
    } else if (step === 3) {
      newSelections.step3 = value;
      newSelections.step4 = null;
    } else if (step === 4) {
      newSelections.step4 = value;
    }

    setSelections(newSelections);
    setCurrentStep(step + 1);
  };

  const handleSubmit = () => {
    const step1Label =
      STEP_1_CORE_STRUGGLES.options.find((o) => o.id === selections.step1)?.label || "";
    const step2Options = selections.step1 ? STEP_2_FOCUS_AREAS[selections.step1]?.options : [];
    const step2Label = step2Options?.find((o) => o.id === selections.step2)?.label || "";
    const step3Options = selections.step2 ? STEP_3_ROOT_CAUSES[selections.step2]?.options : [];
    const step3Label = step3Options?.find((o) => o.id === selections.step3)?.label || "";

    let context = `Agent's core struggle: ${step1Label}. Focus area: ${step2Label}. Root cause: ${step3Label}.`;

    if (selections.step4) {
      context += ` Specific problem: ${selections.step4}.`;
    }

    if (customContext.trim()) {
      context += ` Additional context: ${customContext}`;
    }

    const finalSelections = { ...selections, step5: customContext };
    onComplete(context, finalSelections);
  };

  const goBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const getStepTitle = () => {
    switch (currentStep) {
      case 1:
        return STEP_1_CORE_STRUGGLES.title;
      case 2:
        return selections.step1
          ? STEP_2_FOCUS_AREAS[selections.step1]?.title
          : "";
      case 3:
        return selections.step2
          ? STEP_3_ROOT_CAUSES[selections.step2]?.title
          : "";
      case 4:
        return "Which resonates most?";
      case 5:
        return "Any additional context?";
      default:
        return "";
    }
  };

  const getStepSubtitle = () => {
    switch (currentStep) {
      case 1:
        return STEP_1_CORE_STRUGGLES.subtitle;
      case 2:
        return selections.step1
          ? STEP_2_FOCUS_AREAS[selections.step1]?.subtitle
          : "";
      case 3:
        return selections.step2
          ? STEP_3_ROOT_CAUSES[selections.step2]?.subtitle
          : "";
      case 4:
        return "Select the specific challenge, or skip to customize";
      case 5:
        return "Help us find the perfect episodes";
      default:
        return "";
    }
  };

  const renderProgressBar = () => (
    <div className="flex items-center justify-center mb-12">
      {[1, 2, 3, 4, 5].map((step) => (
        <div key={step} className="flex items-center">
          <div
            className={`w-3 h-3 rounded-full transition-all duration-300 ${
              step < currentStep
                ? "bg-emerald-500"
                : step === currentStep
                ? "bg-kale w-4 h-4"
                : "bg-gray-200"
            }`}
          />
          {step < 5 && (
            <div
              className={`w-12 h-0.5 transition-all duration-300 ${
                step < currentStep ? "bg-emerald-500" : "bg-gray-200"
              }`}
            />
          )}
        </div>
      ))}
    </div>
  );

  const renderBreadcrumbs = () => {
    const crumbs = [];

    if (selections.step1) {
      const label = STEP_1_CORE_STRUGGLES.options.find(
        (o) => o.id === selections.step1
      )?.label;
      crumbs.push(label);
    }
    if (selections.step2 && selections.step1) {
      const label = STEP_2_FOCUS_AREAS[selections.step1]?.options.find(
        (o) => o.id === selections.step2
      )?.label;
      crumbs.push(label);
    }
    if (selections.step3 && selections.step2) {
      const label = STEP_3_ROOT_CAUSES[selections.step2]?.options.find(
        (o) => o.id === selections.step3
      )?.label;
      crumbs.push(label);
    }
    if (selections.step4) {
      crumbs.push(selections.step4);
    }

    if (crumbs.length === 0) return null;

    return (
      <div className="mb-8 flex flex-wrap items-center gap-2">
        {crumbs.map((crumb, idx) => (
          <span key={idx} className="flex items-center">
            {idx > 0 && <span className="text-gray-300 mx-2">→</span>}
            <span className="chip">{crumb}</span>
          </span>
        ))}
      </div>
    );
  };

  const renderOptions = (options: WizardOption[], step: number) => (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-in">
      {options.map((option) => (
        <button
          key={option.id}
          onClick={() => handleSelect(step, option.id)}
          className="card p-6 text-left group cursor-pointer"
        >
          <div className="flex items-start gap-4">
            <span className="text-3xl transition-transform duration-200 group-hover:scale-110">
              {option.icon}
            </span>
            <div className="flex-1">
              <h3 className="font-semibold text-lg text-gray-900 group-hover:text-kale transition-colors">
                {option.label}
              </h3>
              <p className="text-gray-500 mt-1 text-sm leading-relaxed">
                {option.description}
              </p>
            </div>
            <span className="text-gray-300 group-hover:text-kale transition-colors">
              →
            </span>
          </div>
        </button>
      ))}
    </div>
  );

  const renderStep4Problems = () => (
    <div className="space-y-4 animate-fade-in">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {step4Problems.map((problem, idx) => (
          <button
            key={idx}
            onClick={() => handleSelect(4, problem.problem)}
            className="card p-5 text-left group cursor-pointer"
          >
            <h3 className="font-medium text-gray-900 group-hover:text-kale transition-colors mb-2 leading-snug">
              {problem.problem}
            </h3>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">
                {problem.episodes} episode{problem.episodes !== 1 ? "s" : ""}
              </span>
              <span className="text-kale opacity-0 group-hover:opacity-100 transition-opacity text-sm font-medium">
                Select →
              </span>
            </div>
          </button>
        ))}
      </div>

      <button
        onClick={() => setCurrentStep(5)}
        className="w-full p-4 rounded-xl border-2 border-dashed border-gray-200 hover:border-kale/30 text-gray-400 hover:text-kale transition-all text-center text-sm"
      >
        None of these match — let me describe it instead →
      </button>
    </div>
  );

  const renderStep5 = () => (
    <div className="space-y-6 animate-fade-in max-w-xl mx-auto">
      <div className="card p-6">
        <label className="block text-gray-600 text-sm font-medium mb-3">
          Tell us more about this agent's situation
        </label>
        <textarea
          value={customContext}
          onChange={(e) => setCustomContext(e.target.value)}
          placeholder="Example: They've been in the business for 3 years, working about 50 hours a week but only closing 8-10 deals. They feel like they're spinning their wheels..."
          rows={5}
          className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-kale focus:ring-2 focus:ring-kale/10 transition resize-none text-gray-900 placeholder-gray-400"
        />
        <p className="text-xs text-gray-400 mt-3">
          The more detail you provide, the better the recommendations.
        </p>
      </div>

      <button
        onClick={handleSubmit}
        className="btn-primary w-full text-lg flex items-center justify-center gap-2"
      >
        <span>Find the Perfect Episodes</span>
        <span>→</span>
      </button>

      <button
        onClick={() => {
          setCustomContext("");
          handleSubmit();
        }}
        className="w-full text-gray-400 hover:text-kale transition text-sm"
      >
        Skip and search now →
      </button>
    </div>
  );

  return (
    <div className="max-w-3xl mx-auto">
      {renderProgressBar()}

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

      <div className="mb-10 text-center">
        <h2 className="text-3xl md:text-4xl font-semibold text-gray-900 mb-3">
          {getStepTitle()}
        </h2>
        <p className="text-gray-500 text-lg">{getStepSubtitle()}</p>
      </div>

      {currentStep === 1 && renderOptions(STEP_1_CORE_STRUGGLES.options, 1)}

      {currentStep === 2 &&
        selections.step1 &&
        renderOptions(STEP_2_FOCUS_AREAS[selections.step1].options, 2)}

      {currentStep === 3 &&
        selections.step2 &&
        STEP_3_ROOT_CAUSES[selections.step2] &&
        renderOptions(STEP_3_ROOT_CAUSES[selections.step2].options, 3)}

      {currentStep === 4 && renderStep4Problems()}

      {currentStep === 5 && renderStep5()}
    </div>
  );
}
