// Error types
export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public details?: any
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export class ValidationError extends AppError {
  constructor(message: string, details?: any) {
    super(message, 'VALIDATION_ERROR', 400, details);
    this.name = 'ValidationError';
  }
}

export class AuthenticationError extends AppError {
  constructor(message: string = 'Authentication failed') {
    super(message, 'AUTHENTICATION_ERROR', 401);
    this.name = 'AuthenticationError';
  }
}

export class AuthorizationError extends AppError {
  constructor(message: string = 'Not authorized') {
    super(message, 'AUTHORIZATION_ERROR', 403);
    this.name = 'AuthorizationError';
  }
}

export class NotFoundError extends AppError {
  constructor(message: string = 'Resource not found') {
    super(message, 'NOT_FOUND_ERROR', 404);
    this.name = 'NotFoundError';
  }
}

export class ConflictError extends AppError {
  constructor(message: string = 'Resource conflict') {
    super(message, 'CONFLICT_ERROR', 409);
    this.name = 'ConflictError';
  }
}

// Error handler
export class ErrorHandler {
  private static instance: ErrorHandler;
  private errorListeners: ((error: AppError) => void)[] = [];

  private constructor() {}

  static getInstance(): ErrorHandler {
    if (!ErrorHandler.instance) {
      ErrorHandler.instance = new ErrorHandler();
    }
    return ErrorHandler.instance;
  }

  handleError(error: unknown): AppError {
    let appError: AppError;

    if (error instanceof AppError) {
      appError = error;
    } else if (error instanceof Error) {
      appError = new AppError(
        error.message,
        'UNKNOWN_ERROR',
        500,
        { originalError: error }
      );
    } else {
      appError = new AppError(
        'An unknown error occurred',
        'UNKNOWN_ERROR',
        500,
        { originalError: error }
      );
    }

    this.notifyListeners(appError);
    return appError;
  }

  addErrorListener(listener: (error: AppError) => void): () => void {
    this.errorListeners.push(listener);
    return () => {
      this.errorListeners = this.errorListeners.filter((l) => l !== listener);
    };
  }

  private notifyListeners(error: AppError): void {
    this.errorListeners.forEach((listener) => listener(error));
  }
}

// Error utilities
export const isAppError = (error: unknown): error is AppError => {
  return error instanceof AppError;
};

export const getErrorMessage = (error: unknown): string => {
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unknown error occurred';
};

export const getErrorDetails = (error: unknown): any => {
  if (error instanceof AppError) {
    return error.details;
  }
  return null;
};

// Error boundary component props
export interface ErrorBoundaryProps {
  fallback: React.ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}

// Error boundary component
export class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  { hasError: boolean; error: Error | null }
> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }

    return this.props.children;
  }
}

// Error message component
interface ErrorMessageProps {
  error: unknown;
  className?: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ error, className }) => {
  const message = getErrorMessage(error);
  const details = getErrorDetails(error);

  return (
    <div className={className}>
      <p>{message}</p>
      {details && (
        <pre>
          <code>{JSON.stringify(details, null, 2)}</code>
        </pre>
      )}
    </div>
  );
};

// Error toast component
interface ErrorToastProps {
  error: unknown;
  onClose: () => void;
}

export const ErrorToast: React.FC<ErrorToastProps> = ({ error, onClose }) => {
  const message = getErrorMessage(error);

  return (
    <div className="error-toast">
      <div className="error-toast-content">
        <span className="error-toast-message">{message}</span>
        <button className="error-toast-close" onClick={onClose}>
          ×
        </button>
      </div>
    </div>
  );
};

// Error logging service
export class ErrorLogger {
  private static instance: ErrorLogger;

  private constructor() {}

  static getInstance(): ErrorLogger {
    if (!ErrorLogger.instance) {
      ErrorLogger.instance = new ErrorLogger();
    }
    return ErrorLogger.instance;
  }

  logError(error: unknown, context?: any): void {
    const errorMessage = getErrorMessage(error);
    const errorDetails = getErrorDetails(error);

    console.error('Error:', {
      message: errorMessage,
      details: errorDetails,
      context,
      timestamp: new Date().toISOString(),
    });

    // Here you can add additional logging logic, such as sending to a logging service
  }
} 