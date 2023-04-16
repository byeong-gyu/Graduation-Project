package gradu.gradu.dto;

import lombok.*;

import javax.validation.constraints.NotEmpty;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class MemberDTO {

    private Long id;

    private String userID;
    private String userPassID;
    private String userName;
    private String userGender;
    private String userEmail;
    private String userCode;

}
