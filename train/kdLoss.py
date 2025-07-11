import torch.nn as nn

class DistillationLoss(nn.Module):
    def __init__(self, temperature=2.0, alpha=0.5):
        super(DistillationLoss, self).__init__()
        self.temperature = temperature
        self.alpha = alpha
        self.kl = nn.KLDivLoss(reduction="batchmean")
        self.ce = nn.CrossEntropyLoss()

    def forward(self, student_logits, teacher_logits, labels):
        soft_loss = self.kl(
            nn.functional.log_softmax(student_logits / self.temperature, dim=-1),
            nn.functional.softmax(teacher_logits / self.temperature, dim=-1)
        ) * (self.temperature ** 2)


        hard_loss = self.ce(student_logits.reshape(-1, student_logits.size(-1)), labels.reshape(-1))

        return self.alpha * hard_loss + (1 - self.alpha) * soft_loss
