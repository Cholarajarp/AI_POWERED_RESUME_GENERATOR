import React, { useState, useEffect } from 'react';
import { templatesAPI } from '../services/api';
import { Zap, Lock } from 'lucide-react';

export default function Templates() {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [result, setResult] = useState('');

  useEffect(() => {
    const loadTemplates = async () => {
      try {
        const response = await templatesAPI.list();
        setTemplates(response.data);
      } catch (error) {
        console.error('Failed to load templates:', error);
      } finally {
        setLoading(false);
      }
    };
    loadTemplates();
  }, []);

  const handleGenerate = async (template: any) => {
    setGenerating(true);
    try {
      const response = await templatesAPI.generate({
        template_type: template.type,
        resume_content: 'Sample resume',
        job_description: 'Sample job description'
      });
      setResult(response.data.generated_content);
    } catch (error) {
      console.error('Failed to generate:', error);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <main className="p-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-2">AI Templates</h1>
      <p className="text-gray-600 mb-8">
        Generate professional documents using our AI-powered templates
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {templates.map((template: any) => (
          <div
            key={template.id}
            className="bg-white rounded-lg shadow-md hover:shadow-lg transition p-6 cursor-pointer"
            onClick={() => setSelectedTemplate(template)}
          >
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-bold text-gray-900">{template.name}</h3>
                <p className="text-sm text-gray-600 mt-1">{template.description}</p>
              </div>
              {template.is_premium && (
                <Lock className="w-5 h-5 text-yellow-500 flex-shrink-0" />
              )}
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
                {template.type.replace('_', ' ').toUpperCase()}
              </span>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleGenerate(template);
                }}
                disabled={generating}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
              >
                <Zap className="w-4 h-4" />
                Generate
              </button>
            </div>
          </div>
        ))}
      </div>

      {result && (
        <div className="bg-white rounded-lg shadow-md p-6 max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Generated Content</h2>
          <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 max-h-96 overflow-y-auto">
            <p className="text-gray-700 whitespace-pre-wrap">{result}</p>
          </div>
          <button
            onClick={() => navigator.clipboard.writeText(result)}
            className="mt-4 px-6 py-2 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700"
          >
            Copy to Clipboard
          </button>
        </div>
      )}
    </main>
  );
}
