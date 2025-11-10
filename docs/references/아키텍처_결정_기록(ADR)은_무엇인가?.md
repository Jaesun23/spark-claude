# 아키텍처 결정 기록(ADR)은 무엇인가?

## 개요

하나의[아키텍처 결정(AD)](https://en.wikipedia.org/wiki/Architectural_decision)은 아키텍처적으로 중요한 기능적 또는 비기능적 요구사항을 다루는 소프트웨어 설계 선택입니다. 예를 들어, 기술 선택(예: Java vs. JavaScript), IDE 선택(예: IntelliJ vs. Eclipse IDE), 라이브러리 간의 선택(예:[SLF4J](https://www.slf4j.org/)vs[java.util.logging](https://docs.oracle.com/javase/8/docs/api/java/util/logging/package-summary.html)), 또는 기능에 대한 결정(예: 무제한 실행 취소 vs. 제한된 실행 취소). "아키텍처"라는 용어를 너무 심각하게 받아들이거나 너무 강하게 해석하지 마세요. 예시에서 보여주듯이, 아키텍처에 어떤 식으로든 영향을 미칠 수 있는 모든 결정은 아키텍처 결정입니다.

a) 결정을 기록하고 b) 결정을 버전 관리하는 것이 가능한 한 쉬워야 합니다.

## ADR은 어떤 모습일까요?

다음은 아키텍처 결정 기록(ADR) 채택을 결정하기 위한 아키텍처 결정 기록의 예시입니다(마크다운 형식).

```markdown
# 마크다운 아키텍처 결정 기록 사용

## 맥락 및 문제 정의

이 프로젝트에서 내린 아키텍처 결정을 기록하고자 합니다.
이러한 기록은 어떤 형식과 구조를 따라야 할까요?

## 고려된 옵션들

* [MADR](https://adr.github.io/madr/) 2.1.2 – 마크다운 아키텍처 결정 기록
* [Michael Nygard의 템플릿](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions) – "ADR"이라는 용어의 첫 번째 구현체
* [지속 가능한 아키텍처 결정](https://www.infoq.com/articles/sustainable-architectural-design-decisions) – Y-Statements
* <https://github.com/joelparkerhenderson/architecture_decision_record>에 나열된 기타 템플릿들
* 형식 없음 – 파일 형식과 구조에 대한 규칙 없음

## 결정 결과

선택된 옵션: "MADR 2.1.2", 이유는 다음과 같습니다:

* 암묵적 가정들은 명시적으로 만들어져야 합니다.
  설계 문서화는 사람들이 나중에 결정을 이해할 수 있도록 하는 데 중요합니다.
  [합리적 설계 프로세스: 어떻게 그리고 왜 가짜로 만드는가](https://doi.org/10.1109/TSE.1986.6312940)도 참조하세요.
* MADR 형식은 간결하고 우리의 개발 스타일에 적합합니다.
* MADR 구조는 이해하기 쉽고 사용 및 유지보수를 용이하게 합니다.
* MADR 프로젝트는 활발합니다.
* 버전 2.1.2는 ADR 문서화를 시작할 때 사용 가능한 최신 버전입니다.
```

#### 왜 하는가아키텍처 결정 기록 (ADR)?

우리는 이 관행을 다음과 같은 목적으로 사용합니다:

- 과거에 무엇이 수행되었는지 이해하기 위한 빠른 참조 자료 확보
- 우리의 사고와 방법론을 이해관계자들과 공유할 수 있도록 함
- 팀 내부와 외부에서 개방적이고 투명한 소통을 유지하세요

#### 실행 방법아키텍처 결정 기록 (ADR)?

사용 가능한 템플릿들을 살펴보고 이에 대해 읽어보세요. 아래 링크된 템플릿 중 하나를 선택하여 사용하거나, 팀과 조직에 적합한 형식으로 템플릿을 직접 수정하여 만들 수 있습니다.

#### 추천 링크

팀, 고객 또는 이해관계자와 함께아키텍처 결정 기록 (ADR)실무를 좀 더 깊이 있게 운영하는 데 도움이 될 수 있는 훌륭한 링크들을 확인해보세요.

[마크다운 아키텍처 의사결정 기록](https://adr.github.io/madr/)

[지속 가능한 아키텍처 의사결정](https://www.infoq.com/articles/sustainable-architectural-design-decisions/)

[다른 템플릿](https://www.infoq.com/articles/sustainable-architectural-design-decisions/)



# What Is Architectural Decision Records (ADR)?

## Overview

An [Architectural Decision (AD)](https://en.wikipedia.org/wiki/Architectural_decision) is a software design choice that addresses a functional or non-functional requirement that is architecturally significant. This might, for instance, be a technology choice (e.g., Java vs. JavaScript), a choice of the IDE (e.g., IntelliJ vs. Eclipse IDE), a choice between a library (e.g., [SLF4J](https://www.slf4j.org/) vs [java.util.logging](https://docs.oracle.com/javase/8/docs/api/java/util/logging/package-summary.html)), or a decision on features (e.g., infinite undo vs. limited undo). Do not take the term “architecture” too seriously or interpret it too strongly. As the examples illustrate, any decisions that might have an impact on the architecture somehow are architectural decisions.

It should be as easy as possible to a) write down the decisions and b) to version the decisions.

## What Does an ADR Look Like?

Here's an example of an Architectural Decision Record (In Markdown format) for deciding to adopt Architectural Decision Records.

```markdown
# Use Markdown Architectural Decision Records

## Context and Problem Statement

We want to record architectural decisions made in this project.
Which format and structure should these records follow?

## Considered Options

* [MADR](https://adr.github.io/madr/) 2.1.2 – The Markdown Architectural Decision Records
* [Michael Nygard's template](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions) – The first incarnation of the term "ADR"
* [Sustainable Architectural Decisions](https://www.infoq.com/articles/sustainable-architectural-design-decisions) – The Y-Statements
* Other templates listed at <https://github.com/joelparkerhenderson/architecture_decision_record>
* Formless – No conventions for file format and structure

## Decision Outcome

Chosen option: "MADR 2.1.2", because

* Implicit assumptions should be made explicit.
  Design documentation is important to enable people understanding the decisions later on.
  See also [A rational design process: How and why to fake it](https://doi.org/10.1109/TSE.1986.6312940).
* The MADR format is lean and fits our development style.
* The MADR structure is comprehensible and facilitates usage & maintenance.
* The MADR project is vivid.
* Version 2.1.2 is the latest one available when starting to document ADRs.
```

#### Why Do Architectural Decision Records (ADR)?

We use this practice to:

- Have a quick reference to understand what has been done in the past
- Allow us to share our thinking and methods with our stakeholders
- Maintain open and transparent communication inside and outside of our teams

#### How to do Architectural Decision Records (ADR)?

Have a look at some of the available templates and start reading about them. You can choose to use one of the ones linked below or create your own adaptation of the template in a format which works for your team and your organization.

#### Links we love

Check out these great links which can help you dive a little deeper into running the Architectural Decision Records (ADR) practice with your team, customers or stakeholders.

Markdown Architectural Decision Records

Sustainable Architectural Decisions

Other templates