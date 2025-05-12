# MedFlow System Architecture Diagrams

## 1. High-Level System Architecture

```mermaid
graph TB
    subgraph "Patient Interface"
        UI[User Interface]
        Auth[Authentication]
        Upload[Medical Data Upload]
        Chat[Medical Chatbot]
    end

    subgraph "AI Processing Engine"
        SISR[SISR Image Enhancement]
        Classifier[Disease Classification]
        Expert[Expert System]
        NLP[Natural Language Processing]
    end

    subgraph "Output & Recommendations"
        Diagnosis[Diagnosis Generation]
        Treatment[Treatment Recommendations]
        Doctor[Doctor Referral]
        Monitor[Health Monitoring]
    end

    UI --> Auth
    Auth --> Upload
    Upload --> SISR
    Upload --> Classifier
    UI --> Chat
    Chat --> NLP
    NLP --> Expert
    Expert --> Diagnosis
    SISR --> Diagnosis
    Classifier --> Diagnosis
    Diagnosis --> Treatment
    Diagnosis --> Doctor
    Treatment --> Monitor
```

## 2. Patient Journey Flow

```mermaid
flowchart TD
    Start[Patient Entry] --> Login{Login/Register}
    Login -->|New User| Registration[Complete Medical History]
    Login -->|Existing User| Dashboard
    Registration --> Dashboard
    
    Dashboard --> Input{Input Method}
    Input -->|Chatbot| Chat[Describe Symptoms]
    Input -->|Form| Form[Structured Input]
    Input -->|Upload| Upload[Medical Images]
    
    Chat --> Analysis
    Form --> Analysis
    Upload --> Analysis
    
    Analysis --> Diagnosis[AI Diagnosis]
    Diagnosis -->|High Confidence| Treatment[Treatment Plan]
    Diagnosis -->|Low Confidence| Doctor[Doctor Referral]
    
    Treatment --> Monitor[Health Monitoring]
    Doctor --> Monitor
```

## 3. AI Processing Pipeline

```mermaid
flowchart LR
    subgraph "Input Processing"
        Images[Medical Images]
        Symptoms[Symptom Data]
        History[Medical History]
    end

    subgraph "AI Models"
        SISR[SISR Enhancement]
        Classifier[Disease Classification]
        Expert[Expert System]
        NLP[Chatbot Processing]
    end

    subgraph "Output Generation"
        Analysis[Integrated Analysis]
        Diagnosis[Final Diagnosis]
        Recommendations[Treatment Recommendations]
    end

    Images --> SISR
    SISR --> Classifier
    Symptoms --> NLP
    History --> Expert
    NLP --> Expert
    Classifier --> Analysis
    Expert --> Analysis
    Analysis --> Diagnosis
    Diagnosis --> Recommendations
```

## 4. Emergency Response Flow

```mermaid
flowchart TD
    Start[Patient Input] --> Check{Emergency Check}
    Check -->|Emergency Detected| Alert[Emergency Alert]
    Check -->|No Emergency| Normal[Normal Processing]
    
    Alert --> Action[Immediate Action Recommendations]
    Action --> Services[Emergency Services]
    Action --> Family[Family Notification]
    Action --> Doctor[Doctor Alert]
    
    Normal --> Diagnosis[Regular Diagnosis]
```

## 5. Doctor Referral Process

```mermaid
flowchart TD
    Start[AI Diagnosis] --> Need{Need Doctor?}
    Need -->|Yes| Match[Doctor Matching]
    Need -->|No| Self[Self-Care]
    
    Match --> Criteria[Match Criteria]
    Criteria --> Specialization[Medical Specialization]
    Criteria --> Location[Geographic Location]
    Criteria --> Availability[Schedule Availability]
    
    Specialization --> Selection[Doctor Selection]
    Location --> Selection
    Availability --> Selection
    
    Selection --> Contact[Contact Initiation]
    Contact --> Records[Medical Records Sharing]
    Records --> Appointment[Appointment Scheduling]
```

## 6. Health Monitoring System

```mermaid
flowchart TD
    Start[Treatment Plan] --> Monitor[Health Monitoring]
    
    Monitor --> Vitals[Vital Signs]
    Monitor --> Symptoms[Symptom Tracking]
    Monitor --> Medication[Medication Adherence]
    
    Vitals --> Analysis[Trend Analysis]
    Symptoms --> Analysis
    Medication --> Analysis
    
    Analysis --> Alert{Alert Check}
    Alert -->|Issue Detected| Notify[Notification]
    Alert -->|Normal| Continue[Continue Monitoring]
    
    Notify --> Action[Required Action]
    Action --> Update[Update Treatment]
    Action --> Doctor[Doctor Contact]
```

## 7. Information Gathering Flow

```mermaid
flowchart TD
    Start[Patient Entry] --> Initial[Initial Symptom Input]
    Initial --> Chat[Chatbot Interview]
    Chat --> Questions[Targeted Questions]
    Questions --> Tests[Required Tests/Readings]
    Tests --> Analysis[Multi-modal Analysis]
    Analysis --> Diagnosis[Final Diagnosis]

    subgraph "Information Types"
        Symptoms[Symptoms]
        Vitals[Vital Signs]
        Images[Medical Images]
        History[Medical History]
        Lab[Lab Results]
    end

    Symptoms --> Analysis
    Vitals --> Analysis
    Images --> Analysis
    History --> Analysis
    Lab --> Analysis
```

These diagrams provide a visual representation of the MedFlow system's architecture and workflows. Each diagram focuses on a specific aspect of the system, making it easier to understand the different components and their interactions.

The diagrams show:
1. The overall system architecture
2. The patient journey through the system
3. The AI processing pipeline
4. Emergency response procedures
5. Doctor referral process
6. Health monitoring system
7. Information gathering flow

Would you like me to explain any specific diagram in more detail or create additional diagrams for other aspects of the system?

Input Threads:
1. Primary Symptom: Chest pain
2. Location: Left side
3. Duration: 30 minutes
4. Associated Symptoms: Shortness of breath, sweating
5. Vital Signs: Elevated heart rate, blood pressure
6. Medical History: Family history of heart disease

Connection:
- Chest pain + Shortness of breath = Possible cardiac issue
- Elevated vitals support cardiac concern
- Family history increases risk
- System recommends ECG and chest X-ray
